import uuid
from enum import IntEnum

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField()
    co2limit = models.BigIntegerField(null=False)
    costlimit = models.BigIntegerField(null=False)

class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=255, null=False)
    area = models.IntegerField(null=False)
    long = models.DecimalField(null=False, decimal_places=9, max_digits=12)
    lat = models.DecimalField(null=False, decimal_places=9, max_digits=12)

class ComType(IntEnum):
    SupIm = 1
    Demand = 2
    Stock = 3
    Env = 4
    Buy = 5
    Sell = 6

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class DefCommodity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    type = models.IntegerField(choices=ComType.choices(), null=False)
    price = models.IntegerField(null=False)
    max = models.IntegerField(null=False)
    maxperhour = models.IntegerField(null=False)

    def get_com_type_label(self):
        return ComType(self.type).name.title()

class Commodity(DefCommodity):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)

class DefProcess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    instcap = models.IntegerField(null=False)
    caplo = models.IntegerField(null=False)
    maxgrad = models.IntegerField(null=False)
    minfraction = models.IntegerField(null=False)
    invcost = models.IntegerField(null=False)
    fixcost = models.IntegerField(null=False)
    varcost = models.IntegerField(null=False)
    wacc = models.IntegerField(null=False)
    deprecation = models.IntegerField(null=False)
    areapercap = models.IntegerField(null=False)

class Process(DefProcess):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)

class DefProcessCommodity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ratio = models.FloatField(null=False)
    ratiomin = models.FloatField(null=False)

class ProcessCommodity(DefProcessCommodity):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=False)

class DefStorage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    instcapc = models.IntegerField(null=False)
    caploc = models.IntegerField(null=False)
    capupc = models.IntegerField(null=False)
    instcapp = models.IntegerField(null=False)
    caplop = models.IntegerField(null=False)
    capupp = models.IntegerField(null=False)
    effin = models.FloatField(null=False)
    effout = models.FloatField(null=False)
    invcostp = models.IntegerField(null=False)
    invcostc = models.FloatField(null=False)
    fixcostp = models.IntegerField(null=False)
    fixcostc = models.FloatField(null=False)
    varcostp = models.FloatField(null=False)
    varcostc = models.IntegerField(null=False)
    wacc = models.FloatField(null=False)
    deprecation = models.IntegerField(null=False)
    init = models.FloatField(null=False)
    discharge = models.FloatField(null=False)
    epratio = models.FloatField(null=False)


class Storage(DefStorage):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)

class DefDemand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    count = models.IntegerField(null=False)
    steps = models.JSONField(null=False)

class Demand(DefDemand):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)

class DefSuplm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    steps = models.JSONField(null=False)

class Suplm(DefSuplm):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)

class TransType(IntEnum):
    hvac = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Transmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sitein = models.ForeignKey(Site, on_delete=models.CASCADE, null=False, related_name='incoming_transmissions')
    siteout = models.ForeignKey(Site, on_delete=models.CASCADE, null=False, related_name='outgoing_transmissions')
    transmission = models.IntegerField(choices=TransType.choices(), null=False)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    eff = models.FloatField(null=False)
    invcost = models.IntegerField(null=False)
    fixcost = models.IntegerField(null=False)
    varcost = models.FloatField(null=False)
    instcap = models.IntegerField(null=False)
    caplo = models.IntegerField(null=False)
    capup = models.IntegerField(null=False)
    wacc = models.FloatField(null=False)
    deprecation = models.FloatField(null=False)
    reactance = models.FloatField(null=False)
    difflimit = models.FloatField(null=False)
    basevoltage = models.FloatField(null=False)

    def get_trans_type_label(self):
        return ComType(self.transmission).name.title()

class BuySellPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    buy = models.JSONField(null=False)
    sell = models.JSONField(null=False)

class TimeVarEff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=False)
    steps = models.FloatField(null=False)