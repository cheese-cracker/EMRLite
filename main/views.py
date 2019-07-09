# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import requests
# import uuid
import json
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, BillEntry, Bill, Appointment
from django.http import HttpResponse
import datetime
from django.template.loader import get_template


LOGIN_URL = '/main/login'


@login_required(login_url=LOGIN_URL)
def HomeView(req):
    qset = BillEntry.objects.all()
#    print(qset)
    return render(req, 'main/index.html', {
                  'title': 'EMRLite System',
                  'item_list': qset})


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
        try:
            data = req.POST.copy()
            print(data)
        except:
            return HttpResponse('<h2> Incorrect Request Body</h2>')
        try:
            username = data.get('username')
            password = data.get('password')
        except KeyError as missing_data:
            return HttpResponse('<h2> Missing key - {0} </h2>'.format(missing_data))
        doc = authenticate(username=username, password=password)
        if doc is not None:
            login(req, doc)
            try:
                doctor = Doctor.objects.get(user=doc)
            except Exception:
                return HttpResponse('<h2>Profile for this user does not exist!</h2>')
            unique_id = str(doctor.uuid)
            print(unique_id)
            return redirect(reverse(PatientList))
        else:
            return HttpResponse('<h2> Unable to Login</h2>')
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
        data = req.POST.copy()
        print(data)
        selected = int(data['selected'])
        return redirect('/main/cart/{}'.format(selected))


def GenerateBill(req, appointid):
    if req.method == 'POST':
        try:
            data = json.loads(req.body.decode('utf8').replace("'", '"'))
            pass
        except Exception:
            return HttpResponse("<h2>Incorrect Request Body<h2>")
        try:
            patid = appointid.patient.id
            print('Received PatientID {}'.format(str(patid)))
        except Exception:
            return HttpResponse("<h2>Appointment 'ID' not found!<h2>")
        try:
            # Collect Comment
            cment = data['comment']
            # Collect IDs from Bill Items
            idlist = list(data['selected'])
        except KeyError as missing_data:
            return HttpResponse("<h2>Missing key - {0}'<h2>".format(missing_data))

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
            return HttpResponse("<h2>Incorrect Request Body<h2>")
        reqtype = data.get('_method')
        print(reqtype)
        if reqtype == 'POST':
            try:
                name = data.get('name')
                sex = data.get('sex')
                phonenumber = data.get('phonenumber')
                email = data.get('email')
                dob = data.get('dob')
            except KeyError as missing_data:
                return HttpResponse("<h2>Missing key - {0}'<h2>".format(missing_data))
            try:
                entry = Patient()
            except Exception:
                return HttpResponse("<h2>Error in BillEntry model creation<h2>")
            try:
                entry.name = name
                entry.sex = sex
                entry.phone = phonenumber
                entry.email = email
                entry.dob = dob
                print(dob)
            except Exception:
                return HttpResponse("<h2>name is not unique or name, category or price cannot be set to BillEntry<h2>")

            entry.save()
            return redirect('/main/patientlist')
        if reqtype == 'DELETE':
            try:
                idno = data.get('idno')
            except KeyError as missing_data:
                return HttpResponse("<h2>Missing key - {0}'<h2>".format(missing_data))
            try:
                entry = Patient.objects.get(id=idno)
            except Exception:
                return HttpResponse('<h2> 404 Entry not found </h2>')
            entry.delete()

            return redirect('/main/patientlist')
        if reqtype == 'PUT':
            try:
                idno = data.get('idno')
                cost = data.get('cost')
            except KeyError as missing_data:
                return HttpResponse("<h2>Missing key - {0}'<h2>".format(missing_data))
            try:
                entry = BillEntry.objects.get(id=idno)
            except Exception:
                return HttpResponse('<h2> 404 Entry not found </h2>')
            entry.cost = cost
            entry.save()
            return redirect(reverse("AddPatient"))
    else:
        return HttpResponse('<h2> Only POST, PUT and DELETE requests are supported</h2>')


def AddItem(req):
    if req.method == 'POST':
        try:
            data = req.POST.copy()
            print(data)
        except Exception:
            return HttpResponse("<h2>Incorrect Request Body<h2>")
        reqtype = data.get('_method')
        print(reqtype)
        if reqtype == 'POST':
            try:
                name = data.get('name')
                category = data.get('category')
                cost = data.get('cost')
            except KeyError as missing_data:
                return HttpResponse("<h2>Missing key - {0}'<h2>".format(missing_data))
            try:
                entry = BillEntry()
            except Exception:
                return HttpResponse('<h2>Error in BillEntry model creation</h2>')
            try:
                entry.name = name
                entry.category = category
                entry.cost = cost
            except Exception:
                return HttpResponse('<h2>Name is not unique or name, category or price cannot be set to BillEntry</h2>')

            entry.save()

            return redirect('/')
        if reqtype == 'DELETE':
            try:
                name = data.get('name')
                idno = data.get('idno')
            except KeyError as missing_data:
                return HttpResponse('<h2>Missing key - {0}</h2>'.format(missing_data))
            try:
                entry = BillEntry.objects.get(id=idno)
            except Exception:
                return HttpResponse('<h2> 404 Entry not found </h2>')
            entry.delete()

            return redirect('/')
        if reqtype == 'PUT':
            try:
                idno = data.get('idno')
                cost = data.get('cost')
            except KeyError as missing_data:
                return HttpResponse('Missing key - {0}'.format(missing_data))
            try:
                entry = BillEntry.objects.get(id=idno)
            except KeyError as missing_data:
                return HttpResponse('Missing key - {0}'.format(missing_data))
            entry.cost = cost
            entry.save()
            return redirect('/')
    else:
        return HttpResponse('<h2> Only POST, PUT and DELETE requests are supported</h2>')


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
