import os
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from orchestra.forms import widgets
from orchestra.plugins.forms import PluginDataForm

from .. import settings

from . import AppType


help_message = _("Version of PHP used to execute this webapp. <br>"
    "Changing the PHP version may result in application malfunction, "
    "make sure that everything continue to work as expected.")


class PHPAppForm(PluginDataForm):
    php_version = forms.ChoiceField(label=_("PHP version"),
            choices=settings.WEBAPPS_PHP_VERSIONS,
            initial=settings.WEBAPPS_DEFAULT_PHP_VERSION,
            help_text=help_message)


class PHPAppSerializer(serializers.Serializer):
    php_version = serializers.ChoiceField(label=_("PHP version"),
            choices=settings.WEBAPPS_PHP_VERSIONS,
            default=settings.WEBAPPS_DEFAULT_PHP_VERSION,
            help_text=help_message)


class PHPApp(AppType):
    name = 'php'
    verbose_name = "PHP"
    help_text = _("This creates a PHP application under ~/webapps/&lt;app_name&gt;<br>")
    form = PHPAppForm
    serializer = PHPAppSerializer
    icon = 'orchestra/icons/apps/PHP.png'
    
    DEFAULT_PHP_VERSION = settings.WEBAPPS_DEFAULT_PHP_VERSION
    PHP_DISABLED_FUNCTIONS = settings.WEBAPPS_PHP_DISABLED_FUNCTIONS
    PHP_ERROR_LOG_PATH = settings.WEBAPPS_PHP_ERROR_LOG_PATH
    FPM_LISTEN = settings.WEBAPPS_FPM_LISTEN
    FCGID_WRAPPER_PATH = settings.WEBAPPS_FCGID_WRAPPER_PATH
    
    @property
    def is_fpm(self):
        return self.get_php_version().endswith('-fpm')
    
    @property
    def is_fcgid(self):
        return self.get_php_version().endswith('-cgi')
    
    def get_context(self):
        """ context used to format settings """
        return {
            'home': self.instance.account.main_systemuser.get_home(),
            'account': self.instance.account.username,
            'user': self.instance.account.username,
            'app_name': self.instance.name,
        }
    
    def get_php_init_vars(self, per_account=False):
        """
        process php options for inclusion on php.ini
        per_account=True merges all (account, webapp.type) options
        """
        init_vars = {}
        options = self.instance.options.all()
        if per_account:
            options = self.instance.account.webapps.filter(webapp_type=self.instance.type)
        php_options = [option.name for option in type(self).get_php_options()]
        for opt in options:
            if opt.name in php_options:
                init_vars[opt.name] = opt.value
        enabled_functions = []
        for value in options.filter(name='enabled_functions').values_list('value', flat=True):
            enabled_functions += enabled_functions.get().value.split(',')
        if enabled_functions:
            disabled_functions = []
            for function in self.PHP_DISABLED_FUNCTIONS:
                if function not in enabled_functions:
                    disabled_functions.append(function)
            init_vars['dissabled_functions'] = ','.join(disabled_functions)
        if self.PHP_ERROR_LOG_PATH and 'error_log' not in init_vars:
            context = self.get_context()
            error_log_path = os.path.normpath(self.PHP_ERROR_LOG_PATH % context)
            init_vars['error_log'] = error_log_path
        return init_vars
    
    def get_directive(self):
        context = self.get_directive_context()
        if self.is_fpm:
            socket_type = 'unix'
            if ':' in self.FPM_LISTEN:
                socket_type = 'tcp'
            socket = self.FPM_LISTEN % context
            return ('fpm', socket_type, socket, self.instance.get_path())
        elif self.is_fcgid:
            wrapper_path = os.path.normpath(self.FCGID_WRAPPER_PATH % context)
            return ('fcgid', self.instance.get_path(), wrapper_path)
        else:
            raise ValueError("Unknown directive for php version '%s'" % php_version)
    
    def get_php_version(self):
        default_version = self.DEFAULT_PHP_VERSION
        return self.instance.data.get('php_version', default_version)
    
    def get_php_version_number(self):
        php_version = self.get_php_version()
        number = re.findall(r'[0-9]+\.?[0-9]+', php_version)
        if len(number) > 1:
            raise ValueError("Multiple version number matches for '%'" % php_version)
        return number[0]
