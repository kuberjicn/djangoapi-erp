# Generated by Django 4.2 on 2024-01-20 21:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20240121_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('actid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('actname', models.CharField(max_length=150)),
                ('skillname', models.CharField(max_length=100)),
                ('unskillname', models.CharField(max_length=100)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'kuberji_activity',
            },
        ),
        migrations.CreateModel(
            name='AttandanceType',
            fields=[
                ('typ_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('value', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'kuberji_attandancetype',
            },
        ),
        migrations.CreateModel(
            name='DeclareHolidays',
            fields=[
                ('hd_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('hd_date', models.DateField()),
            ],
            options={
                'db_table': 'kuberji_declareholidays',
            },
        ),
        migrations.CreateModel(
            name='DeclareLeaves',
            fields=[
                ('lvs_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('lvs_type', models.CharField(max_length=250)),
                ('value', models.IntegerField(default=0)),
                ('effect_date', models.DateField()),
            ],
            options={
                'db_table': 'kuberji_declareleaves',
            },
        ),
        migrations.CreateModel(
            name='matgroup',
            fields=[
                ('mg_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'kuberji_materialgroup',
            },
        ),
        migrations.CreateModel(
            name='PayrollList',
            fields=[
                ('Pls_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('st_date', models.DateField()),
                ('ed_date', models.DateField()),
                ('islocked', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'kuberji_payrolllist',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('sup_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('sup_name', models.CharField(max_length=450)),
                ('types', models.CharField(blank=True, max_length=45, null=True)),
                ('add1', models.CharField(blank=True, max_length=100, null=True)),
                ('add2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('companyname', models.CharField(blank=True, max_length=100, null=True)),
                ('gstno', models.CharField(blank=True, max_length=25, null=True)),
                ('bloodgroup', models.CharField(blank=True, max_length=25, null=True)),
                ('adharid', models.CharField(blank=True, max_length=25, null=True)),
                ('pan', models.CharField(blank=True, max_length=25, null=True)),
                ('photo', models.FileField(blank=True, null=True, upload_to='profile/')),
                ('adharphoto', models.FileField(blank=True, null=True, upload_to='adhar/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Isactive', models.BooleanField(default=1)),
                ('doj', models.DateField(null=True)),
            ],
            options={
                'db_table': 'kuberji_suppliers',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kuberji_UserProfile',
            },
        ),
        migrations.CreateModel(
            name='SalaryRegister',
            fields=[
                ('sal_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('slry_rate', models.FloatField(default=0.0)),
                ('effect_date', models.DateField()),
                ('ta', models.FloatField(default=0.0)),
                ('da', models.FloatField(default=0.0)),
                ('hra', models.FloatField(default=0.0)),
                ('deleted', models.BooleanField(default=False)),
                ('post', models.CharField(max_length=150, null=True)),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.supplier')),
            ],
            options={
                'db_table': 'kuberji_salaryregister',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('mat_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('mat_name', models.CharField(max_length=150)),
                ('mat_unit', models.CharField(max_length=45)),
                ('HSN', models.CharField(max_length=45)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=15)),
                ('GSTR', models.DecimalField(decimal_places=0, max_digits=2)),
                ('disp', models.CharField(max_length=500)),
                ('gstincluding', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('groupid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.matgroup')),
            ],
            options={
                'db_table': 'kuberji_materials',
            },
        ),
        migrations.CreateModel(
            name='LeaveRegister',
            fields=[
                ('lvr_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ddate', models.DateField()),
                ('leave', models.FloatField(default=0.0)),
                ('lvs_type', models.CharField(max_length=45)),
                ('la_app_id', models.IntegerField(default=0)),
                ('disp', models.CharField(default='by leave granted', max_length=50)),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.supplier')),
            ],
            options={
                'db_table': 'kuberji_leaveregister',
            },
        ),
        migrations.CreateModel(
            name='LeaveApplication',
            fields=[
                ('app_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('app_date', models.DateField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('reason', models.CharField(max_length=500)),
                ('isapproved', models.BooleanField(default=0)),
                ('lvs_type', models.CharField(default='casual', max_length=45)),
                ('contact', models.CharField(max_length=12, null=True)),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.supplier')),
            ],
            options={
                'db_table': 'kuberji_leaveapplication',
            },
        ),
        migrations.CreateModel(
            name='LabourData',
            fields=[
                ('lbr_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ddate', models.DateField()),
                ('skill', models.IntegerField()),
                ('unskill', models.IntegerField()),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('workdetail', models.CharField(max_length=500, null=True)),
                ('actid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.activity')),
                ('siteid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.sites')),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='supdata', to='api.supplier')),
            ],
            options={
                'db_table': 'kuberji_labour',
            },
        ),
        migrations.CreateModel(
            name='InwardOutward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('reg_id', models.CharField(max_length=10)),
                ('inward_date', models.DateField()),
                ('discription', models.CharField(max_length=500)),
                ('in_qty', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('unit', models.CharField(max_length=10)),
                ('received_from', models.CharField(max_length=500, null=True)),
                ('out_qty', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('issue_to', models.CharField(max_length=500, null=True)),
                ('reg_type', models.CharField(default='misc', max_length=10)),
                ('entry_type', models.CharField(default='in', max_length=5)),
                ('isdeleted', models.BooleanField(default=False)),
                ('siteid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.sites')),
            ],
            options={
                'db_table': 'kuberji_inwardoutward',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inv_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ddate', models.DateField()),
                ('qty', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('gstamount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('mat_unit', models.CharField(max_length=10)),
                ('matid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.material')),
                ('siteid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.sites')),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.supplier')),
            ],
            options={
                'db_table': 'kuberji_inventory',
            },
        ),
        migrations.CreateModel(
            name='DetailPayroll',
            fields=[
                ('Par_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('par_date', models.DateField(null=True)),
                ('siteid', models.IntegerField(default=0)),
                ('pr_days', models.IntegerField(default=0, null=True)),
                ('ab_days', models.IntegerField(default=0, null=True)),
                ('cl_days', models.IntegerField(default=0, null=True)),
                ('sl_days', models.IntegerField(default=0, null=True)),
                ('ho_days', models.IntegerField(default=0, null=True)),
                ('slry_rate', models.FloatField(default=0.0)),
                ('payable_days', models.IntegerField(default=0, null=True)),
                ('extra_any', models.FloatField(default=0.0)),
                ('net_slry', models.FloatField(default=0.0)),
                ('bal_cl', models.IntegerField(default=0, null=True)),
                ('bal_sl', models.IntegerField(default=0, null=True)),
                ('Plsid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.payrolllist')),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.supplier')),
            ],
            options={
                'db_table': 'kuberji_detailpayroll',
            },
        ),
        migrations.CreateModel(
            name='Attandance',
            fields=[
                ('att_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('att_date', models.DateField()),
                ('intime', models.TimeField(null=True)),
                ('outtime', models.TimeField(null=True)),
                ('posting_siteid', models.IntegerField(default=0, null=True)),
                ('lat_in', models.FloatField(default=0.0, null=True)),
                ('long_in', models.FloatField(default=0.0, null=True)),
                ('lat_out', models.FloatField(default=0.0, null=True)),
                ('long_out', models.FloatField(default=0.0, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('supid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.supplier')),
                ('typid', models.ForeignKey(default=2, on_delete=django.db.models.deletion.RESTRICT, to='api.attandancetype')),
            ],
            options={
                'db_table': 'kuberji_attandance',
            },
        ),
        migrations.CreateModel(
            name='ActivityQty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('unit', models.CharField(max_length=50)),
                ('qty', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('actid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.activity')),
                ('siteid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.sites')),
            ],
            options={
                'db_table': 'kuberji_activityQty',
            },
        ),
    ]
