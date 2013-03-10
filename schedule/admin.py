from django.contrib import admin
from .models import Week, Task, Shift


class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 0


class WeekAdmin(admin.ModelAdmin):
    inlines = [
        ShiftInline,
    ]


admin.site.register(Week, WeekAdmin)
admin.site.register(Task)
