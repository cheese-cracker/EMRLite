from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
import datetime
from django.template.loader import get_template
from Central.utils import render_to_pdf
from main.models import Patient, Doctor, BillEntry, Bill

#from __future__ import unicode_literals
# import requests
# import uuid
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.views.generic import ListView


#class GeneratePDF(View):
#    def get(self, request, *args, **kwargs):
#        template = get_template('Bill.html')
#        patientfirst = Patient.objects.all()[0]
#        BillEntryfirst=BillEntry.objects.all()[0]
#        context= {
#             'Today': datetime.date.today(),
#            'customer_name': patientfirst.name,
#             'Sex': patientfirst.sex,
#             'product':BillEntryfirst.category,
#             'price' : BillEntryfirst.cost
#        };

#        html = template.render(context)
#        pdf = render_to_pdf('Bill.html', context)
#        return HttpResponse(pdf,content_type='pdf' )



class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
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
            'user': request.user,
            'power': 'Doctor',
            }
        template = get_template('bill.html')
        html = template.render(context)
        pdf = render_to_pdf('bill.html', context)
        return HttpResponse(pdf,content_type='pdf' )

#    res = render(req, 'main/finalbill.html', context)
#    if clearcook:
#        res.delete_cookie('BillID')
#    return res
