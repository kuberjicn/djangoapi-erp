# Generated by Django 5.0 on 2024-02-09 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_salaryregister_supid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='contact',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
