from django.db import models
from django.db.models.fields import DateField, CharField, TextField, AutoField
from django.db.models import ForeignKey
from datetime import date

class Contract(models.Model):
    id = AutoField(primary_key=True)
    nombre = CharField(max_length=250)
    fecha = DateField(default=date.today)

class Rate(models.Model):
    id = AutoField(primary_key=True)
    contract = ForeignKey(Contract, on_delete=models.CASCADE)
    origin = TextField() # POL
    destination = TextField() # POD
    currency = TextField() # Curr.
    twenty = TextField() # 20 GP
    forty = TextField() # 40 GP
    fortyhc = TextField() # 40 HC