from django.contrib import admin
from outings.models import Outing, Event, OutingMember

admin.site.register(Outing)
admin.site.register(Event)
admin.site.register(OutingMember)