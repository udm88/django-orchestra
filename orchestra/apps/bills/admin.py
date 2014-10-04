from django import forms
from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from orchestra.admin import ExtendedModelAdmin
from orchestra.admin.utils import admin_date
from orchestra.apps.accounts.admin import AccountAdminMixin

from . import settings
from .actions import download_bills, view_bill, close_bills, send_bills
from .filters import BillTypeListFilter
from .models import Bill, Invoice, AmendmentInvoice, Fee, AmendmentFee, ProForma, BillLine


PAYMENT_STATE_COLORS = {
    Bill.PAID: 'green',
    Bill.PENDING: 'darkorange',
    Bill.BAD_DEBT: 'red',
}


class BillLineInline(admin.TabularInline):
    model = BillLine
    fields = ('description', 'rate', 'quantity', 'tax', 'subtotal', 'get_total')
    readonly_fields = ('get_total',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.is_open:
            return self.fields
        return super(BillLineInline, self).get_readonly_fields(request, obj=obj)
    
    def has_add_permission(self, request):
        if request.__bill__ and not request.__bill__.is_open:
            return False
        return super(BillLineInline, self).has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        if obj and not obj.is_open:
            return False
        return super(BillLineInline, self).has_delete_permission(request, obj=obj)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Make value input widget bigger """
        if db_field.name == 'description':
            kwargs['widget'] = forms.TextInput(attrs={'size':'110'})
        else:
            kwargs['widget'] = forms.TextInput(attrs={'size':'13'})
        return super(BillLineInline, self).formfield_for_dbfield(db_field, **kwargs)


class BillAdmin(AccountAdminMixin, ExtendedModelAdmin):
    list_display = (
        'number', 'type_link', 'account_link', 'created_on_display',
        'num_lines', 'display_total', 'display_payment_state', 'is_open'
    )
    list_filter = (BillTypeListFilter, 'is_open',)
    add_fields = ('account', 'type', 'is_open', 'due_on', 'comments')
    fieldsets = (
        (None, {
            'fields': ('number', 'display_total', 'account_link', 'type',
                       'display_payment_state', 'is_sent', 'due_on', 'comments'),
        }),
        (_("Raw"), {
            'classes': ('collapse',),
            'fields': ('html',),
        }),
    )
    actions = [download_bills, close_bills, send_bills]
    change_view_actions = [view_bill, download_bills, send_bills, close_bills]
    change_readonly_fields = ('account_link', 'type', 'is_open')
    readonly_fields = ('number', 'display_total', 'is_sent', 'display_payment_state')
    inlines = [BillLineInline]
    
    created_on_display = admin_date('created_on')
    
    def num_lines(self, bill):
        return bill.lines__count
    num_lines.admin_order_field = 'lines__count'
    num_lines.short_description = _("lines")
    
    def display_total(self, bill):
        return "%s &%s;" % (bill.total, settings.BILLS_CURRENCY.lower())
    display_total.allow_tags = True
    display_total.short_description = _("total")
    display_total.admin_order_field = 'total'
    
    def type_link(self, bill):
        bill_type = bill.type.lower()
        url = reverse('admin:bills_%s_changelist' % bill_type)
        return '<a href="%s">%s</a>' % (url, bill.get_type_display())
    type_link.allow_tags = True
    type_link.short_description = _("type")
    type_link.admin_order_field = 'type'
    
    def display_payment_state(self, bill):
        topts = bill.transactions.model._meta
        url = reverse('admin:%s_%s_changelist' % (topts.app_label, topts.module_name))
        url += '?bill=%i' % bill.pk
        state = bill.get_payment_state_display().upper()
        color = PAYMENT_STATE_COLORS.get(bill.payment_state, 'grey')
        return '<a href="{url}" style="color:{color}">{name}</a>'.format(
                url=url, color=color, name=state)
    display_payment_state.allow_tags = True
    display_payment_state.short_description = _("Payment")
    
    def get_readonly_fields(self, request, obj=None):
        fields = super(BillAdmin, self).get_readonly_fields(request, obj=obj)
        if obj and not obj.is_open:
            fields += self.add_fields
        return fields
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BillAdmin, self).get_fieldsets(request, obj=obj)
        if obj and obj.is_open:
            fieldsets = (fieldsets[0],)
        return fieldsets
    
    def get_change_view_actions(self, obj=None):
        actions = super(BillAdmin, self).get_change_view_actions()
        exclude = []
        if obj:
            if not obj.is_open:
                exclude.append('close_bills')
        return [action for action in actions if action.__name__ not in exclude]
    
    def get_inline_instances(self, request, obj=None):
        # Make parent object available for inline.has_add_permission()
        request.__bill__ = obj
        return super(BillAdmin, self).get_inline_instances(request, obj=obj)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Make value input widget bigger """
        if db_field.name == 'comments':
            kwargs['widget'] = forms.Textarea(attrs={'cols': 70, 'rows': 4})
        if db_field.name == 'html':
            kwargs['widget'] = forms.Textarea(attrs={'cols': 150, 'rows': 20})
        return super(BillAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        
    def get_queryset(self, request):
        qs = super(BillAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('lines'))
        qs = qs.prefetch_related('lines', 'lines__sublines')
        return qs
    
    def change_view(self, request, object_id, **kwargs):
        bill = self.get_object(request, unquote(object_id))
        # TODO raise404, here and everywhere
        if not hasattr(bill.account, 'invoicecontact'):
            create_link = reverse('admin:accounts_account_change', args=(bill.account_id,))
            create_link += '#invoicecontact-group'
            messages.warning(request, mark_safe(_(
                'Be aware, related contact doesn\'t have a billing contact defined, '
                'bill can not be generated until one is <a href="%s">provided</a>' % create_link
            )))
        return super(BillAdmin, self).change_view(request, object_id, **kwargs)


admin.site.register(Bill, BillAdmin)
admin.site.register(Invoice, BillAdmin)
admin.site.register(AmendmentInvoice, BillAdmin)
admin.site.register(Fee, BillAdmin)
admin.site.register(AmendmentFee, BillAdmin)
admin.site.register(ProForma, BillAdmin)