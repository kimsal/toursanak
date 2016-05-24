from django.contrib import admin

from .models import *
from super_inlines.admin import SuperInlineModelAdmin,SuperModelAdmin
class ImageAdminInline(admin.TabularInline):
    model = Image
    extra = 1
class TabDetailInlineAdmin(SuperInlineModelAdmin,admin.TabularInline):
	model=TabDetail
	extra=1
class TabAdminInline(SuperInlineModelAdmin,admin.TabularInline):
    model = Tab
    inlines=(TabDetailInlineAdmin,)
    extra = 1
class ScheduleAdminInline(admin.TabularInline):
    model = Schedule
    extra = 1
class TourAdmin(SuperModelAdmin):
    inlines = (ImageAdminInline,TabAdminInline,ScheduleAdminInline)
class TabAdmin(SuperModelAdmin):
	inlines=(TabDetailInlineAdmin,)
admin.site.register(Tour, TourAdmin)
# admin.site.register(Tour)
admin.site.register(Page)
admin.site.register(Category)
# admin.site.register(Image)
admin.site.register(Tab,TabAdmin)