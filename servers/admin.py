from django.contrib import admin
from servers.models import Server, Extra_IP


class IPInline(admin.TabularInline):
    model = Extra_IP


class ServerAdmin(admin.ModelAdmin):
    list_filter = ('name', 'created_at')
    list_display = ('name', 'cost', 'main_ip', 'created_at')
    search_fields = ['name']

    date_hierarchy = 'created_at'
    inlines = [
        IPInline
    ]


admin.site.register(Server, ServerAdmin)