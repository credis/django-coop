# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from coop.models import rdfGraphAll
from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.db.models.loading import get_model
import rdflib
from coop.models import StaticURIModel
from django.db import models
from django.views.decorators.csrf import csrf_exempt

RDF_SERIALIZATIONS = {
    'nt': 'text/plain',
    'n3': 'text/n3',
    'ttl': 'text/turtle',
    'xml': 'application/rdf+xml',
    'json': 'application/json',
    'trix': 'application/trix'
}



def rdfdump(request, model, format):
    if model == 'all':
        g = rdfGraphAll()
    else:
        g = rdfGraphAll(model)
    if format == 'ttl':
        return HttpResponse(g.serialize(format='n3'), mimetype=RDF_SERIALIZATIONS[format])
    elif format == 'json':
        return HttpResponse(g.serialize(format='json-ld'), mimetype=RDF_SERIALIZATIONS[format])
    elif format in RDF_SERIALIZATIONS:
        return HttpResponse(g.serialize(format=format), mimetype=RDF_SERIALIZATIONS[format])


def rdf_import(request):
    rdict = {'models': [], 'pes': settings.PES_HOST}
    models = ['organization', 'article', 'event', 'exchange']
    for name in models:
        cls = get_model('coop_local', name)
        rdict['models'].append({'name': name, 'label': cls.Meta.verbose_name_plural})
    return render_to_response('admin/rdf_import.html', rdict, RequestContext(request))


@csrf_exempt
def import_from_uri(request):
    results = {}
    if request.method == 'POST':
        data = request.POST
        uri = data.get('uri')
        model_name = data.get('model')
        model = get_model('coop_local', model_name)
        if model == None:
            model = get_model('coop_geo', model_name)
        graph_url = data.get('import_rdf_url')
        if graph_url:
            g = rdflib.Grap()
            g.parse(graph_url)
        else:
            g = None
        try:
            (instance, created) = model.get_or_create_from_rdf(uri, g)
            if created:
                results = {"results": "created"} 
            else:
                results = {"results": "updated"} 
        except Exception, e:
            results = {"results": "error", "message": e}
    else:
        results = {"results": "error", "message": "wainting for a POST request"}
    return HttpResponse(json.dumps(results), mimetype="application/json")


