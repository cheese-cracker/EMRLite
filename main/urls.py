from django.conf.urls import url
from .views import PatientListView, PatientList

urlpatterns = [
    url(r'patients', PatientListView.as_view(), name='listpatients'),
    url(r'patientlist', PatientList, name='listofpatients'),
]
