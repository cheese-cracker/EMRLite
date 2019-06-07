from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import datetime
from django.template.loader import get_template
from Central.utils import render_to_pdf #created in step 4
from main.models import Patient,BillEntry

class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('Bill.html')
        patientfirst = Patient.objects.all()[0]
        BillEntryfirst=BillEntry.objects.all()[0]
        context= {
             'Today': datetime.date.today(),
            'customer_name': patientfirst.name,
             'Sex': patientfirst.sex,
             'product':BillEntryfirst.category,
             'price' : BillEntryfirst.cost
        }
        html=template.render(context)
        return HttpResponse(html)
# Create your views here.
