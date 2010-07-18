from django.contrib import admin
from models import Event, Share

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"Conf2010": ("name", )
                          # "open bar all day every day": ("description",),
                          # "Omni Downtown": ("venue",),
                          # "100": ("capacity",)
                           }

#admin.site.register(Event, EventAdmin)
admin.site.register(Event)
admin.site.register(Share)
