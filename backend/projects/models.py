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
    price = models.IntegerField(null=True)
    max = models.IntegerField(null=True)
    maxperhour = models.IntegerField(null=True)

    def get_com_type_label(self):
        return ComType(self.type).name.title()

class Commodity(DefCommodity):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)
    default = models.ForeignKey(DefCommodity, on_delete=models.SET_NULL, null=True, related_name="usages")

class DefProcess(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    instcap = models.FloatField(null=False)
    caplo = models.FloatField(null=False)
    capup = models.FloatField(null=False)
    maxgrad = models.FloatField(null=False)
    minfraction = models.FloatField(null=False)
    invcost = models.FloatField(null=False)
    fixcost = models.FloatField(null=False)
    varcost = models.FloatField(null=False)
    wacc = models.FloatField(null=False)
    deprecation = models.FloatField(null=False)
    areapercap = models.FloatField(null=True)

class Process(DefProcess):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)
    default = models.ForeignKey(DefProcess, on_delete=models.SET_NULL, null=True, related_name="usages")

class ProcComDir(IntEnum):
    In = 1
    Out = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class ProcessCommodityTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direction = models.IntegerField(choices=ProcComDir.choices(), null=False)
    ratio = models.FloatField(null=False)
    ratiomin = models.FloatField(null=True)

    class Meta:
        abstract = True

class DefProcessCommodity(ProcessCommodityTypes):
    def_commodity = models.ForeignKey(DefCommodity, on_delete=models.CASCADE, null=False)
    def_process = models.ForeignKey(DefProcess, on_delete=models.CASCADE, null=False)

class ProcessCommodity(ProcessCommodityTypes):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=False)
    default = models.ForeignKey(DefProcessCommodity, on_delete=models.SET_NULL, null=True, related_name="usages")

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
    epratio = models.FloatField(null=True)


class Storage(DefStorage):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    default = models.ForeignKey(DefStorage, on_delete=models.SET_NULL, null=True, related_name="usages")

class DefDemand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    count = models.IntegerField(null=False)
    steps = models.JSONField(null=False)

class Demand(DefDemand):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    default = models.ForeignKey(DefDemand, on_delete=models.SET_NULL, null=True, related_name="usages")

class DefSuplm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    steps = models.JSONField(null=False)

class Suplm(DefSuplm):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, null=False)
    default = models.ForeignKey(DefSuplm, on_delete=models.SET_NULL, null=True, related_name="usages")

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