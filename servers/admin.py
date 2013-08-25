from django.contrib import admin
from servers.models import Server, Extra_IP, ServerCheck, Purpose, SolusAPI
from django.conf import settings


class IPInline(admin.TabularInline):
    model = Extra_IP


class SolusInline(admin.StackedInline):
    model = SolusAPI


class ServerAdmin(admin.ModelAdmin):
    list_filter = ('name', 'created_at')
    list_display = ('name', 'cost', 'main_ip', 'purchased_at')
    search_fields = ['name']
    filter_horizontal = ('purposes',)

    date_hierarchy = 'purchased_at'
    inlines = [
        SolusInline,
        IPInline
    ]


class ServerCheckAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'online', 'did_change')

admin.site.register(Server, ServerAdmin)
admin.site.register(Purpose)

if settings.DEBUG:
    admin.site.register(SolusAPI)
    admin.site.register(ServerCheck, ServerCheckAdmin)