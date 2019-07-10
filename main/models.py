# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class Doctor(models.Model):
    user = models.OneToOneField(
        'auth.User', on_delete=models.SET_NULL, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    phone = models.BigIntegerField()
    alt_phone = models.BigIntegerField(blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=64)
    sex = models.CharField(max_length=1)
    phone = models.BigIntegerField()
    email = models.EmailField(blank=True)
    dob = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, related_name='appointments')
    time = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    doc = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, related_name='appointments')

    def __str__(self):
         return "{0} - {1}".format(self.patient.name, str(self.time))


class BillEntry(models.Model):
    category = models.CharField(max_length=32, unique=False)
    name = models.CharField(max_length=64, unique=True)
    cost = models.PositiveIntegerField(
        validators=[MaxValueValidator(500000)],
        default=1000)

    def __str__(self):
        return self.name


class Bill(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='billings')
    items = models.ManyToManyField(
        BillEntry, related_name='billings')
    completed = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.person.name
