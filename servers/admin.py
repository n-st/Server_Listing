from django.contrib import admin
from servers.models import Server, Extra_IP, ServerCheck, Purpose


class IPInline(admin.TabularInline):
    model = Extra_IP


class ServerAdmin(admin.ModelAdmin):
    list_filter = ('name', 'created_at')
    list_display = ('name', 'cost', 'main_ip', 'purchased_at')
    search_fields = ['name']

    date_hierarchy = 'purchased_at'
    inlines = [
        IPInline
    ]


class ServerCheckAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'online', 'did_change')

admin.site.register(Server, ServerAdmin)
admin.site.register(ServerCheck, ServerCheckAdmin)
admin.site.register(Purpose)