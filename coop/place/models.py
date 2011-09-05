# -*- coding:utf-8 -*-
from django.db import models
from django_extensions.db import fields as exfields
from django.utils.translation import ugettext_lazy as _

class BaseSite(models.Model):
    title = models.CharField(_('Titre'),null=True,blank=True,max_length=250)
    description = models.TextField(_(u'Description'),null=True,blank=True)
    organization = models.ForeignKey('coop_local.Initiative',null=True,blank=True)
    event = models.ForeignKey('coop_local.Event',null=True,blank=True)
    exchange = models.ForeignKey('coop_local.Exchange',null=True,blank=True)
    site_principal = models.BooleanField(default=True)
    uri = models.CharField(_(u'URI principale'),null=True,blank=True, max_length=250, editable=False)
    adr1 = models.CharField(null=True,blank=True, max_length=100)
    adr2 = models.CharField(null=True,blank=True, max_length=100)
    zipcode = models.CharField(null=True,blank=True, max_length=5)
    city = models.CharField(null=True,blank=True, max_length=100)
    latlong = models.CharField(null=True,blank=True, max_length=100)
    lat = models.CharField(null=True,blank=True, max_length=100)
    long = models.CharField(null=True,blank=True, max_length=100)
    created = exfields.CreationDateTimeField(_(u'Création'),null=True)
    modified = exfields.ModificationDateTimeField(_(u'Modification'),null=True)
    #membre_uri = models.CharField(_(u'Profil FOAF'),blank=True, max_length=250, editable=False)
    uuid = exfields.UUIDField(null=True) #nécessaire pour URI de l'engagement
    class Meta:
        abstract = True
