from django.contrib import admin
from schedule.models import Week, Task, Room, Shift

class RoomAdmin(admin.ModelAdmin):
    list_display = ['number','user']
    list_editable = ['user']

class ShiftInline(admin.TabularInline):
	model = Shift
	extra = 0

class WeekAdmin(admin.ModelAdmin):
    inlines = [
        ShiftInline,
    ]



admin.site.register(Week, WeekAdmin)
admin.site.register(Task)
admin.site.register(Room, RoomAdmin)
