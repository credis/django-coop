# -*- coding:utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django import forms
from coop_local.models import Event, EventCategory, Calendar, Occurrence
from coop.utils.autocomplete_admin import FkAutocompleteAdmin, InlineAutocompleteAdmin
from coop_geo.admin import LocatedInline
from django.db.models.loading import get_model

#from genericadmin.admin import GenericAdminModelAdmin
# GenericStackedInline or GenericTabularInline
# on fera le lien generique depuis l'objet en question si besoin (article, événement)


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('label',)


class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = get_model('coop_local', 'Event')
        #widgets = {'category': chosenwidgets.ChosenSelectMultiple()}

    def __init__(self, *args, **kwargs):
        # initial = {
        #     'event_type': 1, 
        #     'calendar': 1 
        #     }
        # if not kwargs.has_key('initial'):
        # #     kwargs['initial'].update(initial)
        # # else:
        #     kwargs['initial'] = initial
        # Initializing form only after you have set initial dict
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields['calendar'].initial = Calendar.objects.get(id=1)
        self.fields['event_type'].initial = EventCategory.objects.get(id=1)


class EventAdmin(FkAutocompleteAdmin):
    change_form_template = 'admintools_bootstrap/tabbed_change_form.html'
    form = EventAdminForm
    list_display = ('title', 'event_type', 'description')
    list_filter = ('event_type', )
    search_fields = ('title', 'description')
    related_search_fields = {'person': ('last_name', 'first_name',
                                        'email', 'structure', 'username'),
                            'organization': ('title', 'acronym', 'subtitle', 'description'),
                            'location': ('label', 'adr1', 'adr2', 'zipcode', 'city'),
    }
    fieldsets = [['Description', {'fields': ['title', 'description',
        ('event_type', 'calendar'),
        ('organization', 'person'),
        ('location')
      ]}],
    ]

    if "coop_tag" in settings.INSTALLED_APPS:
        fieldsets[0][1]['fields'].insert(2, 'tags')

    inlines = [OccurrenceInline]

admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Calendar)
