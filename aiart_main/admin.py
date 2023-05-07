from django.contrib import admin
from .models import ImagePostReport
# Register your models here.

class ImagePostReportAdmin(admin.ModelAdmin):
    model = ImagePostReport
    readonly_fields= ('imagepost', 'report_date','report_option','other_option','user')
    list_display = ('imagepost', 'report_date')


admin.site.register(ImagePostReport, ImagePostReportAdmin)