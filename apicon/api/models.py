from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser,User

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token



    
class Material(models.Model):
    mat_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    mat_name = models.CharField(max_length=150)
    mat_unit = models.CharField(max_length=45)
    HSN = models.CharField(max_length=45)
    rate = models.DecimalField(max_digits=15, decimal_places=2)
    GSTR = models.DecimalField(max_digits=2, decimal_places=0)
    disp = models.CharField(max_length=500)
    groupid = models.ForeignKey("matgroup",  on_delete=models.CASCADE)
    gstincluding = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "kuberji_materials"
    def __str__(self) :
        return self.mat_name

class matgroup(models.Model):
    mg_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "kuberji_materialgroup"
    def __str__(self) :
        return self.name

class Supplier(models.Model):
    sup_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=True)
    sup_name = models.CharField(max_length=450)
    types = models.CharField(max_length=45 ,null=True,blank=True)
    add1 = models.CharField(max_length=100, null=True,blank=True)
    add2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    companyname = models.CharField(max_length=100, null=True,blank=True)
    gstno = models.CharField(max_length=25, null=True,blank=True)
    bloodgroup = models.CharField(max_length=25, null=True,blank=True)
    adharid = models.CharField(max_length=25, null=True,blank=True)
    pan = models.CharField(max_length=25, null=True,blank=True)
    photo = models.FileField(upload_to='profile/', null=True,blank=True)
    adharphoto = models.FileField(upload_to='adhar/', null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    Isactive = models.BooleanField(default=1)
    doj = models.DateField(null=True)

    class Meta:
        db_table = "kuberji_suppliers"
    def __str__(self):
        return self.sup_name
    

class Company(models.Model):
    comp_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=True)
    compname = models.CharField(max_length=150)
    email = models.EmailField(max_length=45, null=True)
    phone = models.CharField(max_length=45, null=True)
    contactperson = models.CharField(max_length=150, null=True)
    PAN = models.CharField(max_length=45, null=True)
    GST = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = "kuberji_company"
    def __str__(self) :
        return self.compname

class Sites(models.Model):
    site_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    sitename = models.CharField(max_length=100)
    add1 = models.CharField(max_length=100, null=True ,blank=True)
    add2 = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=45, null=True ,blank=True)
    state = models.CharField(max_length=45, null=True,blank=True)
    email = models.EmailField(max_length=45, null=True)
    phone = models.CharField(max_length=45, null=True)
    contactperson = models.CharField(max_length=150, null=True ,blank=True)
    Isactive = models.BooleanField()
    compid = models.ForeignKey(Company,  on_delete=models.CASCADE)

    class Meta:
        db_table = "kuberji_site"
    def __str__(self) :
        return self.sitename

class Inventory(models.Model):
    inv_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    supid = models.ForeignKey(Supplier,  on_delete=models.CASCADE)
    matid = models.ForeignKey(Material,   on_delete=models.CASCADE)
    ddate = models.DateField()
    qty = models.DecimalField(blank=True, null=True,
                              max_digits=10, decimal_places=2)
    rate = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    amount = models.DecimalField(
        blank=True, null=True, max_digits=15, decimal_places=2)
    gstamount = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)
    siteid = models.ForeignKey(Sites,   on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    mat_unit = models.CharField(max_length=10)

    class Meta:
        db_table = "kuberji_inventory"

    @property
    def total_amount(self):
        value = 0
        value += self.amount + self.gstamount  # sum(self.amount)
       # calculate value based on model instance represented by self
        return value


class InwardOutward(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    reg_id = models.CharField(max_length=10)
    inward_date = models.DateField()
    discription = models.CharField(max_length=500)
    in_qty = models.DecimalField(
        max_digits=10, decimal_places=2, default=00000000.00)
    unit = models.CharField(max_length=10)
    received_from = models.CharField(max_length=500, null=True)
    out_qty = models.DecimalField(
        max_digits=10, decimal_places=2, default=00000000.00)
    issue_to = models.CharField(max_length=500, null=True)
    reg_type = models.CharField(max_length=10, default="misc")
    entry_type = models.CharField(max_length=5, default="in")
    siteid = models.ForeignKey(Sites,   on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'kuberji_inwardoutward'


class Activity(models.Model):
    actid = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    actname = models.CharField(max_length=150)
    skillname = models.CharField(max_length=100)
    unskillname = models.CharField(max_length=100)
    created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'kuberji_activity'
    def __str__(self) :
        return self.actname

class ActivityQty(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    siteid = models.ForeignKey(Sites,   on_delete=models.CASCADE)
    actid = models.ForeignKey(Activity,   on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    qty = models.DecimalField(
        max_digits=10, decimal_places=2, default=00000000.00)
    rate = models.DecimalField(
        max_digits=10, decimal_places=2, default=00000000.00)
    created = models.DateTimeField(default=datetime.now)

    @property
    def amount(self):
        return ([self.qty * self.rate])

    class Meta:
        db_table = 'kuberji_activityQty'


class LabourData(models.Model):
    lbr_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    ddate = models.DateField()
    supid = models.ForeignKey(
        Supplier,   on_delete=models.CASCADE, related_name='supdata')
    siteid = models.ForeignKey(Sites,   on_delete=models.CASCADE)
    actid = models.ForeignKey(Activity,   on_delete=models.CASCADE)
    skill = models.IntegerField()
    unskill = models.IntegerField()
    created = models.DateTimeField(default=datetime.now)
    workdetail = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'kuberji_labour'
    def __str__(self) :
        return self.ddate

 # when DeclareHolidays update attandance also update for all active employee


class DeclareHolidays(models.Model):
    hd_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=250)
    hd_date = models.DateField()

    class Meta:
        db_table = 'kuberji_declareholidays'
    def __str__(self) :
        return self.name


class AttandanceType(models.Model):
    typ_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=10)

    class Meta:
        db_table = 'kuberji_attandancetype'
    def __str__(self) :
        return self.name
#  new employee created at that time Attandance also updated


class Attandance(models.Model):
    att_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    att_date = models.DateField()
    intime = models.TimeField(null=True)
    outtime = models.TimeField(null=True)
    timediff = models.FloatField(default=0.0, null=True)
    supid = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    fhType= models.ForeignKey(AttandanceType, on_delete=models.CASCADE, default=2,related_name='attandance_fh')
    shType = models.ForeignKey(AttandanceType, on_delete=models.CASCADE, default=2,related_name='attandance_sh')
    posting_siteid = models.IntegerField(null=True, default=0)
    lat_in = models.DecimalField( max_digits=20, decimal_places=2,default=0,null=True)
    long_in = models.DecimalField( max_digits=20, decimal_places=2,default=0,null=True)
    lat_out = models.DecimalField( max_digits=20, decimal_places=2,default=0,null=True)
    long_out =models.DecimalField( max_digits=20, decimal_places=2,default=0,null=True)
    username = models.CharField(max_length=100, null=True)

    @property
    def timediff(self):
        start = datetime.combine(datetime.today(), self.intime)
        end = datetime.combine(datetime.today(), self.outtime)
        delta = end - start
        return delta.seconds // 3600

    class Meta:
        db_table = 'kuberji_attandance'
        ordering=['-att_date']
    def __str__(self) :
        return self.att_date

class PayrollList(models.Model):
    Pls_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    st_date = models.DateField()
    ed_date = models.DateField()
    islocked = models.BooleanField(default=0)

    class Meta:
        db_table = 'kuberji_payrolllist'


class DetailPayroll(models.Model):
    Par_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    par_date = models.DateField(null=True)
    Plsid = models.ForeignKey(PayrollList, on_delete=models.CASCADE)
    supid = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    siteid = models.IntegerField(default=0)
    pr_days = models.IntegerField(default=0, null=True)
    ab_days = models.IntegerField(default=0, null=True)
    cl_days = models.IntegerField(default=0, null=True)
    sl_days = models.IntegerField(default=0, null=True)
    ho_days = models.IntegerField(default=0, null=True)
    slry_rate = models.FloatField(default=0.0)
    payable_days = models.IntegerField(default=0, null=True)
    extra_any = models.FloatField(default=0.0)
    net_slry = models.FloatField(default=0.0)
    bal_cl = models.IntegerField(default=0, null=True)
    bal_sl = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'kuberji_detailpayroll'
    def __str__(self) :
        return self.par_date

class SalaryRegister(models.Model):
    sal_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    supid = models.ForeignKey(Supplier,related_name='suppliers', on_delete=models.CASCADE)
    slry_rate = models.FloatField(default=0.0)
    effect_date = models.DateField()
    ta = models.FloatField(default=0.0)
    da = models.FloatField(default=0.0)
    hra = models.FloatField(default=0.0)
    deleted = models.BooleanField(default=False)
    post = models.CharField(max_length=150, null=True ,blank=True)

    class Meta:
        db_table = 'kuberji_salaryregister'
        ordering = ['supid__sup_name']
       

# when DeclareLeaves table update , data also updated in leavesregister to all active employee
# also new employee created at that time leaveregister also updated
class DeclareLeaves(models.Model):
    lvs_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    lvs_type = models.CharField(max_length=250)
    value = models.IntegerField(default=0)
    effect_date = models.DateField()

    class Meta:
        db_table = 'kuberji_declareleaves'


class LeaveRegister(models.Model):
    lvr_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    supid = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ddate = models.DateField()
    leave = models.FloatField(default=0.0)
    lvs_type = models.CharField(max_length=45)
    la_app_id = models.IntegerField(default=0)
    disp = models.CharField(default='by leave granted', max_length=50)

    @property
    def totcl(self):
        if self.lvs_type == 4:
            sum_cl = sum(self.leave)
        return sum_cl

    @property
    def totsl(self):
        if self.lvs_type == 5:
            sum_sl = sum(self.leave)
        return sum_sl

    class Meta:
        db_table = 'kuberji_leaveregister'
    def __str__(self) :
        return self.ddate


class LeaveApplication(models.Model):
    app_id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False)
    app_date = models.DateField()
    from_date = models.DateField()
    
    supid = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    reason = models.CharField(max_length=500)
    isapproved = models.BooleanField(default=0)
    lvs_type = models.CharField(max_length=45, default='casual')
    contact = models.CharField(max_length=12,blank=True, null=True)

    @property
    def totdays(self):
        delta = self.to_date - self.from_date
        return delta.days+1

    class Meta:
        db_table = 'kuberji_leaveapplication'
    def __str__(self) :
        return self.app_date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        db_table = "kuberji_UserProfile"
    
