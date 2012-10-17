from django.contrib import admin
from schedule.models import Week, Task, Room, Shift

admin.site.register(Week)
admin.site.register(Task)
admin.site.register(Room)
admin.site.register(Shift)
