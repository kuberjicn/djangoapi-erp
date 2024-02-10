# Generated by Django 4.2 on 2024-02-10 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_leaveapplication_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attandance',
            name='typid',
        ),
        migrations.RemoveField(
            model_name='leaveapplication',
            name='to_date',
        ),
        migrations.AddField(
            model_name='attandance',
            name='fhType',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='attandance_fh', to='api.attandancetype'),
        ),
        migrations.AddField(
            model_name='attandance',
            name='shType',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='attandance_sh', to='api.attandancetype'),
        ),
        migrations.AlterField(
            model_name='attandance',
            name='lat_in',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='attandance',
            name='lat_out',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='attandance',
            name='long_in',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='attandance',
            name='long_out',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]
