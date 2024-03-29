# Generated by Django 4.2.9 on 2024-01-15 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('factory_id', models.AutoField(primary_key=True, serialize=False)),
                ('factory_name', models.CharField(max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('location_name', models.CharField(max_length=256)),
                ('x_coordinate', models.IntegerField()),
                ('y_coordinate', models.IntegerField()),
                ('factory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='fleet.factory')),
                ('north', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='south_of', to='fleet.location')),
                ('northeast', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='southwest_of', to='fleet.location')),
                ('northwest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='southeast_of', to='fleet.location')),
                ('south', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='north_of', to='fleet.location')),
                ('southeast', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='northwest_of', to='fleet.location')),
                ('southwest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='northeast_of', to='fleet.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('robot_id', models.AutoField(primary_key=True, serialize=False)),
                ('robot_name', models.CharField(max_length=256, null=True)),
                ('is_idle', models.BooleanField(default=True)),
                ('current_location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fleet.location')),
                ('factory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.factory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(null=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('robot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fleet.robot')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Obstacle',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('obstacle_id', models.AutoField(primary_key=True, serialize=False)),
                ('obstacle_type', models.CharField(choices=[('ASSEMBLY LINE', 'ASSEMBLY LINE'), ('TABLE', 'TABLE'), ('CHAIR', 'CHAIR')], default='ASSEMBLY LINE', max_length=256)),
                ('current_location', models.ManyToManyField(to='fleet.location')),
                ('factory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet.factory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
