# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import requests
import uuid
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.views.generic import ListView
from .models import Patient, Doctor


def HomeView(req):
    return render(req, 'main/index.html')


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
    return render(req, 'main/table.html', context)


def Login(req):
    if req.method == 'POST':
        # print(req.body.decode('utf-8').replace("''", '""'))
        try:
            # Coz we use " for quotes
            # data = json.loads(req.body)
            data = req.POST.copy()
            print(data)
        except:
            return JsonResponse(
                {"message": "Incorrect Request Body", "status": 403}
            )
        try:
            # username = data['name']
            # password = data['password']
            username = data.get('username')
            password = data.get('password')
        except KeyError as missing_data:
            return JsonResponse(
                {'message': 'Missing key - {0}'.format(missing_data),
                 "status": 3}
            )
        doc = authenticate(username=username, password=password)
        if doc is not None:
            login(req, doc)
            try:
                doctor = Doctor.objects.get(user=doc)
            except:
                return JsonResponse(
                    {'message': 'Profile for this user does not exist!',
                     'status': 404}
                )
            unique_id = str(doctor.uuid)
            print(unique_id)
            return JsonResponse(
                {"message": "Logged in Successfully!",
                 "status": 1,
                 "user_id": unique_id}
            )
        else:
            return JsonResponse(
                {'message': 'Invalid Login Credentials',
                 "status": 0}
            )
    elif req.method == 'GET':
        return render(req, 'main/login.html', {'title': 'Doctor Login'})
