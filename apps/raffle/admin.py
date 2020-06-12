from django.contrib import admin

from apps.raffle.models import Contest, Prize


class ContestAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'start', 'end', 'win_at', 'prize')
    readonly_fields = ('win_at',)
    ordering = ('-end', 'code')


class PrizeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'perday')
    ordering = ('code',)


admin.site.register(Contest, ContestAdmin)
admin.site.register(Prize, PrizeAdmin)
