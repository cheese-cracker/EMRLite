from django.conf.urls import url
from .views import PatientList, Login, LogoutReq

urlpatterns = [
    # url(r'patients', PatientListView.as_view(), name='listpatients'),
    url(r'^patientlist/', PatientList, name='listofpatients'),
    url(r'^login/?', Login, name='login'),
    url(r'^logout/?', LogoutReq, name='logout'),
]
