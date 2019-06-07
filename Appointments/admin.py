from django.contrib import admin
from Appointments.models import AccessRecord,DocName,PatientInfo
# Register your models here.
admin.site.register(AccessRecord)
admin.site.register(DocName)
admin.site.register(PatientInfo)
