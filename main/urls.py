from django.conf.urls import url
from .views import (
    PatientList,
    Login,
    LogoutReq,
    AddItem,
    BillList,
    PatientSelectView,
)

urlpatterns = [
    # url(r'patients', PatientListView.as_view(), name='listpatients'),
    url(r'^patientlist/', PatientList, name='listofpatients'),
    url(r'^login/?', Login, name='login'),
    url(r'^logout/?', LogoutReq, name='logout'),
    url(r'^add_item/?', AddItem, name='add_item'),
    url(r'^billhistory/?', BillList, name='listofbills'),
    url(r'^patientselector/?', PatientSelectView, name='patientselect'),
]
