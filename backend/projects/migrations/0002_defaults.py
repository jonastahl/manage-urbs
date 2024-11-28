# Generated by Django 5.1.2 on 2024-11-08 09:44

from django.db import migrations

from projects.models import ComType, ProcComDir


def load_defaults(apps, schema_editor):
    def_commodity = apps.get_model('projects', 'DefCommodity')
    solar = def_commodity(name='Solar', type=ComType.SupIm)
    solar.save()
    wind = def_commodity(name='Wind', type=ComType.SupIm)
    wind.save()
    hydro = def_commodity(name='Hydro', type=ComType.SupIm)
    hydro.save()
    diesel = def_commodity(name='Diesel', type=ComType.Stock, price=4, max=-1, maxperhour=-1)
    diesel.save()
    elec = def_commodity(name='Elec', type=ComType.Demand)
    elec.save()
    co2 = def_commodity(name='CO2', type=ComType.Env, price=0, max=-1, maxperhour=-1)
    co2.save()

    def_process = apps.get_model('projects', 'DefProcess')
    photovoltaics = def_process(name='Photovoltaics', description='Generates electricity from sun', instcap=0, caplo=15000, capup=160000, maxgrad=-1, minfraction=0, invcost=600000, fixcost=12000, varcost=0, wacc=0.07, depreciation=25, areapercap=14000)
    photovoltaics.save()
    wind_park = def_process(name='Wind park', description='Generates electricity from wind', instcap=0, caplo=0, capup=13000, maxgrad=-1, minfraction=0, invcost=1500000, fixcost=30000, varcost=0, wacc=0.07, depreciation=25)
    wind_park.save()
    hydro_plant = def_process(name='Hydro plant', description='Generates electricity from water', instcap=0, caplo=0, capup=1400, maxgrad=-1, minfraction=0, invcost=1600000, fixcost=20000, varcost=0, wacc=0.07, depreciation=50)
    hydro_plant.save()
    diesel_generator = def_process(name='Diesel Generator', description='Generates electricity from diesel while generating CO2', instcap=0, caplo=0, capup=80000, maxgrad=4.8, minfraction=0.25, invcost=450000, fixcost=6000, varcost=1.6, wacc=0.07, depreciation=30)
    diesel_generator.save()
    slack = def_process(name='Curtailpower', description='Consumes overproduced electricity', instcap=0, caplo=0, capup=999999, maxgrad=-1, minfraction=0, invcost=0, fixcost=0, varcost=0, wacc=0, depreciation=1)
    slack.save()

    def_process_commodity = apps.get_model('projects', 'DefProcessCommodity')
    photovoltaics_solar = def_process_commodity(def_process=photovoltaics, def_commodity=solar, direction=ProcComDir.In, ratio=1.0)
    photovoltaics_solar.save()
    photovoltaics_elec = def_process_commodity(def_process=photovoltaics, def_commodity=elec, direction=ProcComDir.Out, ratio=1.0)
    photovoltaics_elec.save()
    wind_park_wind = def_process_commodity(def_process=wind_park, def_commodity=wind, direction=ProcComDir.In, ratio=1.0)
    wind_park_wind.save()
    wind_park_elec = def_process_commodity(def_process=wind_park, def_commodity=elec, direction=ProcComDir.Out, ratio=1.0)
    wind_park_elec.save()
    hydro_plant_hydro = def_process_commodity(def_process=hydro_plant, def_commodity=hydro, direction=ProcComDir.In, ratio=1.0)
    hydro_plant_hydro.save()
    hydro_plant_elec = def_process_commodity(def_process=hydro_plant, def_commodity=elec, direction=ProcComDir.Out, ratio=1.0)
    hydro_plant_elec.save()
    diesel_generator_diesel = def_process_commodity(def_process=diesel_generator, def_commodity=diesel, direction=ProcComDir.In, ratio=1.0, ratiomin=1.2)
    diesel_generator_diesel.save()
    diesel_generator_elec = def_process_commodity(def_process=diesel_generator, def_commodity=elec, direction=ProcComDir.Out, ratio=0.6)
    diesel_generator_elec.save()
    diesel_generator_co2 = def_process_commodity(def_process=diesel_generator, def_commodity=co2, direction=ProcComDir.Out, ratio=0.2, ratiomin=0.24)
    diesel_generator_co2.save()
    slack_elec = def_process_commodity(def_process=slack, def_commodity=elec, direction=ProcComDir.In, ratio=1)
    slack_elec.save()

    def_storage = apps.get_model('projects', 'DefStorage')
    battery = def_storage(name='Battery', description='Example battery', def_commodity=elec, instcapc=0, caploc=0, capupc=-1, instcapp=0, caplop=0, capupp=-1, effin=0.80, effout=0.80, invcostp=1000, invcostc=9.7, fixcostp=0, fixcostc=0, varcostp=0, varcostc=0, wacc=0.007, depreciation=50, init=0.5, discharge=0.0000035)
    battery.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_defaults),
    ]
