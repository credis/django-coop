# -*- coding:utf-8 -*-
from django.contrib import admin
from django import forms
from coop.exchange.models import BaseTransaction, BaseProduct

from django.db.models.loading import get_model
from django.utils.translation import ugettext_lazy as _
from coop.utils.autocomplete_admin import FkAutocompleteAdmin, InlineAutocompleteAdmin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from coop_geo.admin import LocatedInline
from tinymce.widgets import AdminTinyMCE
from coop.utils.fields import MultiSelectFormField, MethodsCheckboxSelectMultiple, DomainCheckboxSelectMultiple
from coop.exchange.models import ETYPE

# class PaymentInline(admin.TabularInline):
#     model = get_model('coop_local', 'PaymentModality')
#     #model = BasePaymentModality
#     extra = 0


class ExchangeMethodForm(forms.ModelForm):
    etypes = MultiSelectFormField(widget=DomainCheckboxSelectMultiple(), choices=ETYPE.CHOICES)

    class Meta:
        model = get_model('coop_local', 'ExchangeMethod')


class ExchangeMethodAdmin(admin.ModelAdmin):  # AdminImageMixin,
    form = ExchangeMethodForm
    list_display = ('label', 'applications')


class ExchangeForm(forms.ModelForm):
    description = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 60}), required=False)
    methods = forms.ModelMultipleChoiceField(   queryset=get_model('coop_local', 'ExchangeMethod').objects.all(),
                                                widget=MethodsCheckboxSelectMultiple(), 
                                                required=False) 
    
    def __init__(self, *args, **kwargs):
        super(ExchangeForm, self).__init__(*args, **kwargs)
    #   self.fields['methods'].widget = forms.CheckboxSelectMultiple()
        self.fields['methods'].help_text = ''
        self.fields['tags'].label = 'Tags'

    class Media:
        js = ('js/select_exchange_methods.js',)
        
    class Meta:
        model = get_model('coop_local', 'Exchange')


class ExchangeInline(admin.StackedInline):
    form = ExchangeForm
    model = get_model('coop_local', 'Exchange')
    fieldsets = ((None, {'fields': (('eway', 'etype'),
                                     'methods',
                                     'title',
                                    'description', 'tags',
                                    'location', 'area')
                        }),)
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'location':
            kwargs['queryset'] = self.parent_object.locations()
        if db_field.name == 'area':
            kwargs['queryset'] = self.parent_object.areas()    
        return super(ExchangeInline, self).formfield_for_dbfield(db_field, **kwargs)

    def __init__(self, *args, **kwargs):
        self.parent_object = kwargs['obj']
        del kwargs['obj']  # superclass will choke on this
        super(ExchangeInline, self).__init__(*args, **kwargs)


class ProductInline(admin.StackedInline):
    model = BaseProduct
    fieldsets = ((None, {'fields': ('title',
                                    'description',
                                    )}),)
    extra = 1


class TransactionInline(admin.StackedInline):
    model = BaseTransaction
    fk_name = 'destination_org'
    fieldsets = ((None, {'fields': ('title', 'origin', 'description')}),)
    #related_search_fields = {'origin': ('title', 'description', 'organization__title'), }
    extra = 1


class ExchangeAdmin(ForeignKeyAutocompleteAdmin):  # AdminImageMixin,
    form = ExchangeForm
    list_display = ('title', 'etype') #, 'methods')
    # TODO to be finished does not work ...
    # list_editable = ('methods',)
    related_search_fields = {'organization': ('title', 'subtitle', 'description'), }
    fieldsets = ((None, {'fields': (('eway', 'etype'),
                                     'methods',
                                     'title',
                                     'organization',
                                    'description', 'tags')
                        }),)
    inlines = [
            #PaymentInline,
            LocatedInline,  # Using coop-geo
        ]
