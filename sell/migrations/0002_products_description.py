# Generated by Django 4.0.6 on 2022-11-14 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='description',
            field=models.CharField(default='description not available', max_length=500),
        ),
    ]