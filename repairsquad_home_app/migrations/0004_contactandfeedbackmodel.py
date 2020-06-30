# Generated by Django 3.0.7 on 2020-06-24 15:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('repairsquad_home_app', '0003_auto_20200616_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactAndFeedbackModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('attended_to', models.BooleanField(default=False)),
                ('requested_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
