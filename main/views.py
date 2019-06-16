# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import requests
# import uuid
import json
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.views.generic import ListView
from .models import Patient, Doctor, BillEntry, Bill


LOGIN_URL = '/main/login'


def HomeView(req):
    return render(req, 'main/index.html')


@login_required(login_url=LOGIN_URL)
def PatientList(req):
    qset = Patient.objects.all()
    context = {
        'title': 'PatientList',
        'patientList': qset,
        'user': req.user,
        'power': 'Doctor',
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
            # return render(req, 'main/table.html', context)
            return redirect(reverse(PatientList))
            # return JsonResponse(
            #     {"message": "Logged in Successfully!",
            #      "status": 1,
            #      "user_id": unique_id}
            # )
        else:
            return JsonResponse(
                {'message': 'Invalid Login Credentials',
                 "status": 0}
            )
    elif req.method == 'GET':
        return render(req, 'main/login.html', {'title': 'Doctor Login'})


def LogoutReq(req):
    logout(req)
    return redirect(reverse(HomeView))


@login_required(login_url=LOGIN_URL)
def FinalBillView(req):
    clearcook = 0
    try:
        billid = req.COOKIES['BillID']
        print('Received BillID {}'.format(str(billid)))
        clearcook = 1
    except Exception:
        print('Cookie Not Found')
        return JsonResponse(
           {"message": "Cookie 'PatientID' not found!", "status": 553}
        )
    lastbill = Bill.objects.get(id=billid)
    context = {
        'title': 'Bill View',
        'bill': lastbill,
        'itemlist': lastbill.items.all(),
        'patient': lastbill.person,
        'user': req.user,
        'power': 'Doctor',
    }
    res = render(req, 'main/finalbill.html', context)
    if clearcook:
        res.delete_cookie('BillID')
    return res


def CartView(req):
    patname = 'None'
    context = {
        'title': 'Bill Addition',
        'item_list': BillEntry.objects.all(),
        'patient': patname,
    }
    try:
        # patid = req.POST['selected']
        patid = req.COOKIES['PatientID']
        patname = Patient.objects.get(id=patid).name
    except Exception:
        print('No PatientID Cookie Found')
        # return JsonResponse({
        #     "message": "Cookie 'PatientID' not found.",
        #     "status": 493})
    return render(req, 'main/cart.html', context)


@login_required(login_url=LOGIN_URL)
def AddItem(req):
    if req.method == 'POST':
        try:
            data = req.POST.copy()
            print(data)
        except Exception:
            return JsonResponse(
                {"message": "Incorrect Request Body", "status": 403}
            )
        reqtype = data.get('_method')
        print(reqtype)
        if reqtype == 'POST':
            try:
                name = data.get('name')
                category = data.get('category')
                cost = data.get('cost')
            except KeyError as missing_data:
                return JsonResponse(
                    {'message': 'Missing key - {0}'.format(missing_data),
                     "status": 3}
                )
            try:
                entry = BillEntry()
            except Exception:
                return JsonResponse(
                    {'message': 'Error in BillEntry model creation', 'status': 500}
                )
            try:
                entry.name = name
                entry.category = category
                entry.cost = cost
            except Exception:
                return JsonResponse(
                    {
                        'message': 'name is not unique or name, category or price cannot be set to BillEntry',
                        'status': 3
                    }
                )

            entry.save()
            return JsonResponse(
                {"message": "Successfully added item", "status": 1})
        if reqtype == 'DELETE':
            try:
                name = data.get('name')
                idno = data.get('idno')
            except KeyError as missing_data:
                return JsonResponse(
                    {'message': 'Missing key - {0}'.format(missing_data),
                     "status": 3})
            try:
                entry = BillEntry.objects.get(id=idno)
            except Exception:
                return JsonResponse(
                    {'message': 'Entry not found',
                     "status": 404})
            entry.delete()

            return JsonResponse(
                    {'message': 'Successfully deleted item',
                     'status': 1})
        if reqtype == 'PUT':
            try:
                idno = data.get('idno')
                cost = data.get('cost')
            except KeyError as missing_data:
                return JsonResponse(
                    {'message': 'Missing key - {0}'.format(missing_data),
                     "status": 3})
            try:
                entry = BillEntry.objects.get(id=idno)
            except Exception:
                return JsonResponse(
                    {'message': 'Entry not found',
                     "status": 404})
            entry.cost = cost
            entry.save()
            return JsonResponse(
                    {'message': 'Successfully changed cost of item',
                     'status': 1})
    else:
        return JsonResponse(
            {'message': 'Only POST, PUT and DELETE requests are supported',
             'status': 403})


@login_required(login_url=LOGIN_URL)
def BillList(req):
    qset = Bill.objects.order_by('-id')[:100]
    context = {
        'title': 'Bill History',
        'queryset': qset,
        'user': req.user,
        'power': 'Doctor',
    }
    return render(req, 'main/billlist.html', context)


def PatientSelectView(req):
    context = {
        'title': 'Patient Selector',
        'queryset': Patient.objects.all(),
    }
    if req.method == 'GET':
        return render(req, 'main/patientselector.html', context)
    elif req.method == 'POST':
        # res = render(req, 'main/patientselector.html', context)
        try:
            data = req.POST.copy()
            print(data)
            selected = int(data['selected'])
        except Exception:
            return JsonResponse(
                {"message": "Incorrect Request Body or missing",
                 "status": 403})
        res = redirect(reverse(CartView))
        if 'PatientID' not in req.COOKIES:
            res.set_cookie('PatientID', selected)
        return res


# Only For Testing!
def TestView(req):
    data = req.POST.copy()
    print(data)
    selected = data.get('id[]')
    # data = json.loads(req.POST)
    # selected = data['selected']
    print(selected)
    return JsonResponse(
        {'requested': data,
         'technique': req.method}
    )
