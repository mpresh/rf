from django.contrib import admin
from models import Entity, EntityType, AttributeType, Attribute

class EntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"Conf2010": ("name", )
                          # "open bar all day every day": ("description",),
                          # "Omni Downtown": ("venue",),
                          # "100": ("capacity",)
                           }

#admin.site.register(Event, EventAdmin)
admin.site.register(Entity)
admin.site.register(EntityType)
admin.site.register(AttributeType)
admin.site.register(Attribute)
