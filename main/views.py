# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# from django.views.generic import ListView
from .models import Patient

'''
Class is inherits from ListView
which has
- queryset for the items
- as_view() (to represent as function view in urls.py)
- template has to have same name
'''
# class PatientListView(ListView):
#     queryset = Patient.objects.all()


def PatientList(req):
    qset = Patient.objects.all()
    context = {
        'title': 'PatientList',
        'patientList': qset,
    }
    return render(req,'main/table.html',context)
