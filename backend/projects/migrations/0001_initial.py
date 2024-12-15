# Generated by Django 5.1.3 on 2024-12-15 15:27

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'SupIm'), (2, 'Demand'), (3, 'Stock'), (4, 'Env'), (5, 'Buy'), (6, 'Sell')])),
                ('price', models.IntegerField(null=True)),
                ('max', models.IntegerField(null=True)),
                ('maxperhour', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefCommodity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'SupIm'), (2, 'Demand'), (3, 'Stock'), (4, 'Env'), (5, 'Buy'), (6, 'Sell')])),
                ('price', models.IntegerField(null=True)),
                ('max', models.IntegerField(null=True)),
                ('maxperhour', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('autoquery', models.IntegerField(choices=[(1, 'Solar'), (2, 'Wind')], null=True)),
                ('autoadd', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefDemand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('steps', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefProcess',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('instcap', models.FloatField()),
                ('caplo', models.FloatField()),
                ('capup', models.FloatField()),
                ('maxgrad', models.FloatField()),
                ('minfraction', models.FloatField()),
                ('invcost', models.FloatField()),
                ('fixcost', models.FloatField()),
                ('varcost', models.FloatField()),
                ('wacc', models.FloatField()),
                ('depreciation', models.FloatField()),
                ('areapercap', models.FloatField(null=True)),
                ('autoadd', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefSupIm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('steps', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('instcap', models.FloatField()),
                ('caplo', models.FloatField()),
                ('capup', models.FloatField()),
                ('maxgrad', models.FloatField()),
                ('minfraction', models.FloatField()),
                ('invcost', models.FloatField()),
                ('fixcost', models.FloatField()),
                ('varcost', models.FloatField()),
                ('wacc', models.FloatField()),
                ('depreciation', models.FloatField()),
                ('areapercap', models.FloatField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BuySellPrice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('buy', models.JSONField()),
                ('sell', models.JSONField()),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.commodity')),
            ],
        ),
        migrations.AddField(
            model_name='commodity',
            name='defcommodity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usages', to='projects.defcommodity'),
        ),
        migrations.CreateModel(
            name='DefProcessCommodity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('direction', models.IntegerField(choices=[(1, 'In'), (2, 'Out')])),
                ('ratio', models.FloatField()),
                ('ratiomin', models.FloatField(null=True)),
                ('def_commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.defcommodity')),
                ('def_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.defprocess')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DefStorage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('instcapc', models.IntegerField()),
                ('caploc', models.IntegerField()),
                ('capupc', models.IntegerField()),
                ('instcapp', models.IntegerField()),
                ('caplop', models.IntegerField()),
                ('capupp', models.IntegerField()),
                ('effin', models.FloatField()),
                ('effout', models.FloatField()),
                ('invcostp', models.IntegerField()),
                ('invcostc', models.FloatField()),
                ('fixcostp', models.IntegerField()),
                ('fixcostc', models.FloatField()),
                ('varcostp', models.FloatField()),
                ('varcostc', models.IntegerField()),
                ('wacc', models.FloatField()),
                ('depreciation', models.IntegerField()),
                ('init', models.FloatField()),
                ('discharge', models.FloatField()),
                ('epratio', models.FloatField(null=True)),
                ('autoadd', models.BooleanField(default=False)),
                ('def_commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.defcommodity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('steps', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.commodity')),
                ('defdemand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usages', to='projects.defdemand')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessCommodity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('direction', models.IntegerField(choices=[(1, 'In'), (2, 'Out')])),
                ('ratio', models.FloatField()),
                ('ratiomin', models.FloatField(null=True)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.commodity')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.process')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('co2limit', models.BigIntegerField()),
                ('costlimit', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('config', models.JSONField()),
                ('status', models.IntegerField(choices=[(1, 'Optimal'), (2, 'Infeasible'), (3, 'Error')], null=True)),
                ('result', models.JSONField(null=True)),
                ('log', models.TextField(null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('area', models.IntegerField(null=True)),
                ('lon', models.DecimalField(decimal_places=9, max_digits=12)),
                ('lat', models.DecimalField(decimal_places=9, max_digits=12)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.site'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.site'),
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('instcapc', models.IntegerField()),
                ('caploc', models.IntegerField()),
                ('capupc', models.IntegerField()),
                ('instcapp', models.IntegerField()),
                ('caplop', models.IntegerField()),
                ('capupp', models.IntegerField()),
                ('effin', models.FloatField()),
                ('effout', models.FloatField()),
                ('invcostp', models.IntegerField()),
                ('invcostc', models.FloatField()),
                ('fixcostp', models.IntegerField()),
                ('fixcostc', models.FloatField()),
                ('varcostp', models.FloatField()),
                ('varcostc', models.IntegerField()),
                ('wacc', models.FloatField()),
                ('depreciation', models.IntegerField()),
                ('init', models.FloatField()),
                ('discharge', models.FloatField()),
                ('epratio', models.FloatField(null=True)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.commodity')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupIm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('steps', models.JSONField()),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.commodity')),
                ('defsupim', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usages', to='projects.defsupim')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimeVarEff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('steps', models.FloatField()),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.process')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.site')),
            ],
        ),
        migrations.CreateModel(
            name='Transmission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transmission', models.IntegerField(choices=[(1, 'hvac')])),
                ('eff', models.FloatField()),
                ('invcost', models.IntegerField()),
                ('fixcost', models.IntegerField()),
                ('varcost', models.FloatField()),
                ('instcap', models.IntegerField()),
                ('caplo', models.IntegerField()),
                ('capup', models.IntegerField()),
                ('wacc', models.FloatField()),
                ('depreciation', models.FloatField()),
                ('reactance', models.FloatField()),
                ('difflimit', models.FloatField()),
                ('basevoltage', models.FloatField()),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.commodity')),
                ('sitein', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transmissions', to='projects.site')),
                ('siteout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_transmissions', to='projects.site')),
            ],
        ),
    ]
