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


class Patient(models.Model):
    name = models.CharField(max_length=64)
    sex = models.CharField(max_length=1)
    phone = models.BigIntegerField()
    email = models.EmailField(unique=True, blank=True)


class BillEntry(models.Model):
    category = models.CharField(max_length=32, unique=False)
    name = models.CharField(max_length=64, unique=True)
    cost = models.PositiveIntegerField(
        validators=[MaxValueValidator(500000)],
        default=1000)


class Bill(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='billings')
    items = models.ManyToManyField(
        BillEntry, related_name='billings')
    comment = models.TextField(blank=True)
