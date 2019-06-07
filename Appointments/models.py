from django.db import models

class DocName(models.Model):
    top_name = models.CharField(max_length=264,unique=True)

    def __str__(self):
        return self.top_name

class PatientInfo(models.Model):
    topic=models.ForeignKey(DocName, on_delete = models.PROTECT)
    name=models.CharField(max_length=264,unique=True)
    PhoneNo=models.CharField(max_length=11,unique=True)

class AccessRecord(models.Model):
    name=models.ForeignKey(PatientInfo,on_delete = models.PROTECT)
    date=models.DateField()

    def __str__(self):
        return str(self.date)

# Create your models here.
