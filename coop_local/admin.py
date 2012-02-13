# -*- coding:utf-8 -*-
from django.contrib import admin
from coop_local.models import Membre,MemberCategory, Role,Engagement, \
    OrganizationCategory, Initiative, SeeAlsoLink, SameAsLink, Relation,\
    Exchange, PaymentModality
from coop.admin import LocatedInline, AreaInline, BaseEngagementInline, \
    BaseInitiativeAdminForm, BaseInitiativeAdmin, BaseMembreAdmin, \
    BaseRelationInline, BaseEngInitInline, BaseExchangeInline, \
    BaseExchangeAdmin, BasePaymentInline

from coop.utils.autocomplete_admin import FkAutocompleteAdmin,InlineAutocompleteAdmin

admin.site.register(Role)
admin.site.register(MemberCategory)
admin.site.register(OrganizationCategory)

#from genericadmin.admin import GenericAdminModelAdmin,GenericTabularInline
from django.contrib.contenttypes.generic import GenericTabularInline


class SeeAlsoInline(GenericTabularInline):
    model = SeeAlsoLink
    extra=1
    
class SameAsInline(GenericTabularInline):
    model = SameAsLink
    extra=1    

class PaymentInline(BasePaymentInline):
    model = PaymentModality
    extra = 0

class ExchangeInline(BaseExchangeInline):
    model = Exchange
    extra=1    

class EngagementInline(BaseEngagementInline,InlineAutocompleteAdmin):
    model = Engagement

class RelationInline(BaseRelationInline,InlineAutocompleteAdmin):
    model = Relation

class InitiativeAdminForm(BaseInitiativeAdminForm):
    class Meta:
        model = Initiative


class InitiativeAdmin(BaseInitiativeAdmin,FkAutocompleteAdmin):
    form = InitiativeAdminForm
    inlines = [
        EngagementInline,
        ExchangeInline,
        LocatedInline,
        AreaInline,
        SeeAlsoInline,
        RelationInline
        ]
    fieldsets = BaseInitiativeAdmin.fieldsets + (
    ('CREDIS', {'fields': (('statut','secteur_fse'),('siret','naf'))}),
    )    
    
admin.site.register(Initiative, InitiativeAdmin)

class MembreAdmin(BaseMembreAdmin):
    inlines = [
           LocatedInline, 
           #BaseEngInitInline,
           #SeeAlsoInline,SameAsInline
        ]

admin.site.register(Membre, MembreAdmin)


class ExchangeAdmin(BaseExchangeAdmin):
    fieldsets = ((None, {
            'fields' : ('etype',('permanent','expiration',),'title','description',
                        #'tags',
                        'org'
                       )
            }),)
    inlines = [
            PaymentInline,
            LocatedInline, 
        ]

admin.site.register(Exchange, ExchangeAdmin)

#admin.site.register(PaymentModality)


# class SiteAdmin(BaseSiteAdmin):
#      form = SiteForm
# 
# admin.site.register(Site, SiteAdmin)


from coop_cms.admin import ArticleAdmin as CmsArticleAdmin

class ArticleAdmin(CmsArticleAdmin):
    fieldsets = CmsArticleAdmin.fieldsets + (
        ('Misc', {'fields': ('author',)}),
    )

from coop_cms.settings import get_article_class
admin.site.unregister(get_article_class())
admin.site.register(get_article_class(), ArticleAdmin)




