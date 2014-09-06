from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from orchestra.core import accounts
from orchestra.models.queryset import group_by

from . import settings
from .methods import PaymentMethod


class PaymentSourcesQueryset(models.QuerySet):
    def get_default(self):
        return self.filter(is_active=True).first()


class PaymentSource(models.Model):
    account = models.ForeignKey('accounts.Account', verbose_name=_("account"),
            related_name='paymentsources')
    method = models.CharField(_("method"), max_length=32,
            choices=PaymentMethod.get_plugin_choices())
    data = JSONField(_("data"))
    is_active = models.BooleanField(_("is active"), default=True)
    
    objects = PaymentSourcesQueryset.as_manager()
    
    def __unicode__(self):
        return "%s (%s)" % (self.label, self.method_class.verbose_name)
    
    @cached_property
    def method_class(self):
        return PaymentMethod.get_plugin(self.method)
    
    @cached_property
    def label(self):
        return self.method_class().get_label(self.data)
    
    @cached_property
    def number(self):
        return self.method_class().get_number(self.data)
    
    def get_bill_context(self):
        method = self.method_class()
        return {
            'message': method.get_bill_message(self),
        }
    
    def get_due_delta(self):
        return self.method_class().due_delta


class TransactionQuerySet(models.QuerySet):
    group_by = group_by
    
    def create(self, **kwargs):
        source = kwargs.get('source')
        if source is None or not hasattr(source.method_class, 'process'):
            # Manual payments don't need processing
            kwargs['state']=self.model.WAITTING_CONFIRMATION
        return super(TransactionQuerySet, self).create(**kwargs)


# TODO lock transaction in waiting confirmation
class Transaction(models.Model):
    WAITTING_PROCESSING = 'WAITTING_PROCESSING' # CREATED
    WAITTING_CONFIRMATION = 'WAITTING_CONFIRMATION' # PROCESSED
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    DISCARTED = 'DISCARTED'
    SECURED = 'SECURED'
    STATES = (
        (WAITTING_PROCESSING, _("Waitting processing")),
        (WAITTING_CONFIRMATION, _("Waitting confirmation")),
        (CONFIRMED, _("Confirmed")),
        (REJECTED, _("Rejected")),
        (SECURED, _("Secured")),
        (DISCARTED, _("Discarted")),
    )
    
    objects = TransactionQuerySet.as_manager()
    
    bill = models.ForeignKey('bills.bill', verbose_name=_("bill"),
            related_name='transactions')
    source = models.ForeignKey(PaymentSource, null=True, blank=True,
            verbose_name=_("source"), related_name='transactions')
    process = models.ForeignKey('payments.TransactionProcess', null=True,
            blank=True, verbose_name=_("process"), related_name='transactions')
    state = models.CharField(_("state"), max_length=32, choices=STATES,
            default=WAITTING_PROCESSING)
    amount = models.DecimalField(_("amount"), max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default=settings.PAYMENT_CURRENCY)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "Transaction {}".format(self.id)
    
    @property
    def account(self):
        return self.bill.account


class TransactionProcess(models.Model):
    """
    Stores arbitrary data generated by payment methods while processing transactions
    """
    data = JSONField(_("data"), blank=True)
    file = models.FileField(_("file"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    
    class Meta:
        verbose_name_plural = _("Transaction processes")
    
    def __unicode__(self):
        return str(self.id)


accounts.register(PaymentSource)
accounts.register(Transaction)
