from django.contrib import admin
from schedule.models import Week, Task, Room, Shift

class RoomAdmin(admin.ModelAdmin):
    list_display = ['number','user']
    list_editable = ['user']

admin.site.register(Week)
admin.site.register(Task)
admin.site.register(Room, RoomAdmin)
admin.site.register(Shift)
