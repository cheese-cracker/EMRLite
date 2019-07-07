# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Doctor, Patient, Bill, BillEntry
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PatientResource(resources.ModelResource):
    class Meta:
        model=Patient

class PatientAdmin(ImportExportModelAdmin):
    resource_class=PatientResource

admin.site.register(Doctor)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Bill)
admin.site.register(BillEntry)
