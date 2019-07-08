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
from .models import Patient, Doctor, BillEntry, Bill, Appointment
from django.http import HttpResponse
import datetime
from django.template.loader import get_template


LOGIN_URL = '/main/login'


@login_required(login_url=LOGIN_URL)
def HomeView(req):
    return render(req, 'main/index.html',
                  {'title': 'EMRLite System',
                   'usr': req.user})


@login_required(login_url=LOGIN_URL)
def PatientList(req):
    qset = Patient.objects.all()
    context = {
        'title': 'PatientList',
        'patientList': qset,
        'usr': req.user,
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
    return redirect(reverse(Login))


@login_required(login_url=LOGIN_URL)
def FinalBillView(req, billid):
    try:
        lastbill = Bill.objects.get(id=billid)
    except Exception:
        err = '<h1> Error 404 Bill with id {} not found!</h1>'.format(billid)
        return HttpResponse(err, req)
    context = {
        'title': 'Bill View',
        'bill': lastbill,
        'itemlist': lastbill.items.all(),
        'patient': lastbill.person,
        'usr': req.user,
        'power': 'Doctor',
    }
    if req.method == 'GET':
        res = render(req, 'main/finalbill.html', context)
        return res
    elif req.method == 'POST':
        template = get_template('main/bill3.html')
        html = template.render(context)
        res = HttpResponse(html, req)
        lastbill.completed = 1
        lastbill.save()
        return res
    else:
        return HttpResponse('<h1>Request Method Not Supported</h1>', req)
    #    pdf = render_to_pdf('main/bill.html', context)
    #    return httpresponse(pdf,content_type='pdf' )


def CartView(req, appointid):
    try:
        appoint = Appointment.objects.get(id=appointid)
        context = {
            'title': 'Bill Addition',
            'item_list': BillEntry.objects.all(),
            'patient': appoint.patient.name,
            'extras': 1,
        }
    except Exception:
        context = {
            'title': 'TEST Bill Addition',
            'item_list': BillEntry.objects.all(),
            'patient': 'APPOINTMENT NOT FOUND',
            'extras': 1,
        }
        print('No Appointment ID found!')
    return render(req, 'main/cart.html', context)


def AppointListView(req):
    today = datetime.date.today()
    # qset = Appointment.objects.all()
    qset = Appointment.objects.filter(
        time__year=today.year,
        time__month=today.month,
        time__day=today.day,
    )
    context = {
        'title': 'Appointment View',
        'queryset': qset,
        'usr': req.user,
        'extras': 1,
    }
    if req.method == 'GET':
        return render(req, 'main/appointselect.html', context)
    elif req.method == 'POST':
        # try:
        data = req.POST.copy()
        print(data)
        selected = int(data['selected'])
        return redirect('/main/cart/{}'.format(selected))
        # except Exception:
        #     return JsonResponse(
        #         {"message": "Incorrect Request Body or unable to received",
        #          "status": 403})


def GenerateBill(req, appointid):
    if req.method == 'POST':
        # clearcook = 0
        try:
            data = json.loads(req.body.decode('utf8').replace("'", '"'))
            # data = req.POST.copy()
            pass
        except Exception:
            return JsonResponse(
               {"message": "Incorrect Request Body", "status": 403}
            )
        try:
            patid = appointid.patient.id
            print('Received PatientID {}'.format(str(patid)))
            # clearcook = 1
        except Exception:
            return JsonResponse(
               {"message": "Appointment 'ID' not found!", "status": 404}
            )
        try:
            # Collect Comment
            cment = data['comment']
            # Collect IDs from Bill Items
            idlist = list(data['selected'])
        except KeyError as missing_data:
            return JsonResponse(
                {'message': 'Missing key - {0}'.format(missing_data),
                 "status": 3})

        # Create Bill and modify and save (to get id)
        patient = Patient.objects.get(id=patid)
        customerbill = Bill(person=patient, comment=cment)
        customerbill.save()

        # Add Items corresponding to each id selected
        for idno in idlist:
            itemtaken = BillEntry.objects.get(id=idno)
            print(itemtaken.name)
            customerbill.items.add(itemtaken)

        # Save Generated Bill Again
        customerbill.save()

        res = redirect('/main/bill/{}'.format(customerbill.id))
        # if clearcook:
            # res.delete_cookie('PatientID')
        return res
    elif req.method == 'GET':
        return redirect(reverse(BillList))


@login_required(login_url=LOGIN_URL)
def AddPatient(req):
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
                sex = data.get('sex')
                phonenumber = data.get('phonenumber')
                email=data.get('email')
                # excelbackup(name,sex,phonenumber,email)
            except KeyError as missing_data:
                return JsonResponse(
                    {'message': 'Missing key - {0}'.format(missing_data),
                     "status": 3}
                )
            try:
                entry = Patient()
            except Exception:
                return JsonResponse(
                    {'message': 'Error in BillEntry model creation', 'status': 500}
                )
            try:
                entry.name = name
                entry.sex = sex
                entry.phone = phonenumber
                entry.email=email
            except Exception:
                return JsonResponse(
                    {
                        'message': 'name is not unique or name, category or price cannot be set to BillEntry',
                        'status': 3
                    }
                )

            entry.save()
            return redirect('/main/patientlist')
        if reqtype == 'DELETE':
            try:
                idno = data.get('idno')
            except KeyError as missing_data:
                return JsonResponse(
                    {'message': 'Missing key - {0}'.format(missing_data),
                     "status": 3})
            try:
                entry = Patient.objects.get(id=idno)
            except Exception:
                return JsonResponse(
                    {'message': 'Entry not found',
                     "status": 404})
            entry.delete()

            return redirect('/main/patientlist')
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

            return redirect('/')
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

            return redirect('/')
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
            return redirect('/')
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
        'usr': req.user,
        'power': 'Doctor',
    }
    return render(req, 'main/billlist.html', context)


@login_required(login_url=LOGIN_URL)
def PatientSelectView(req):
    context = {
        'title': 'Patient Selector',
        'queryset': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'today': str(datetime.date.today()),
        'extras': 1,
        'usr':req.user
    }
    if req.method == 'GET':
        return render(req, 'main/patientselector.html', context)
    elif req.method == 'POST':
        # res = render(req, 'main/patientselector.html', context)
        try:
            data = req.POST.copy()
            print(data)
            selected = int(data['selected'])
            docSelected = int(data['doctor'])
            datetimeSelected = str(data['date']) + " " + str(data['time'])
        except Exception:
            return HttpResponse('<h2> Field is Missing. Make Sure you fill all fields</h2><h5>Incorrect Request Body')
        try:
            patObj = Patient.objects.get(id=selected)
            docObj = Doctor.objects.get(id=docSelected)
        except Exception:
            return HttpResponse("<h1> ERROR: Patient or Doctor with id Not Found!</h1>")
        newappoint = Appointment(
                        patient=patObj,
                        doc=docObj,
                        time=datetimeSelected,
                                )
        newappoint.save()

        res = redirect(reverse(AppointListView))
        # res = redirect('/main/cart/{}'.format(newappoint.id))
        # res.set_cookie('PatientID', selected)
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
