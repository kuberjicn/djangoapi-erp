
from  api.models import Sites,Company,Supplier,SalaryRegister,LeaveRegister,LeaveApplication,UserProfile,Material,matgroup,Inventory,Attandance,AttandanceType
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.forms.models import model_to_dict


class CompanySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ='__all__' 
        ordering=['compname']

class SiteSerilizer(serializers.ModelSerializer):
    #compid_id=serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), source='compid', write_only=True)
    compid=CompanySerilizer()
    class Meta:
        model = Sites
        fields ='__all__' 

    

    def create(self, validated_data):
         compid_data = validated_data.pop('compid')
         compid_instance = Company.objects.get(**compid_data)
         sites_instance = Sites.objects.create(compid=compid_instance, **validated_data)
         return sites_instance
    def update(self, instance, validated_data):
        compid_data = validated_data.pop('compid', {})
        compid_instance= Company.objects.get(**compid_data)
        instance.sitename = validated_data.get('sitename', instance.sitename)
        instance.add1 = validated_data.get('add1', instance.add1)
        instance.add2 = validated_data.get('add2', instance.add2)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.contactperson = validated_data.get('contactperson', instance.contactperson)
        instance.Isactive = validated_data.get('Isactive', instance.Isactive)
        instance.compid = compid_instance
        instance.save()
        return instance
    
    
class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['url', 'username', 'email', 'groups','first_name']
    

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class SupplierSerilizer(serializers.ModelSerializer):
   
    class Meta:
        model = Supplier
        fields ='__all__' 
    

    def create(self, validated_data):
        return Supplier.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.sup_name = validated_data.get('sup_name', instance.sup_name)
        instance.types = validated_data.get('types', instance.types)
        instance.add1 = validated_data.get('add1', instance.add1)
        instance.add2 = validated_data.get('add2', instance.add2)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.companyname = validated_data.get('companyname', instance.companyname)
        instance.gstno = validated_data.get('gstno', instance.gstno)
        instance.bloodgroup = validated_data.get('bloodgroup', instance.bloodgroup)
        instance.adharid = validated_data.get('adharid', instance.adharid)
        instance.pan = validated_data.get('pan', instance.pan)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.adharphoto = validated_data.get('adharphoto', instance.adharphoto)
        instance.Isactive = validated_data.get('Isactive', instance.Isactive)
        instance.doj = validated_data.get('doj', instance.doj)
        instance.save()
        return instance
    
class SalaryRegisterSerilizer(serializers.ModelSerializer):
    supid = SupplierSerilizer( read_only=True)
    supid_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supid', write_only=True)
    
    class Meta:
        model = SalaryRegister
        fields ='__all__'
        ordering=['supid__sup_name']

    # def create(self, validated_data):
    #     #print(validated_data)
    #     return SalaryRegister.objects.create(**validated_data)
   

class LeaveRegisterSerializer(serializers.ModelSerializer):
    supid=SupplierSerilizer(read_only=True)
    class Meta:
        model=LeaveRegister
        fields="__all__"
        
class LeaveApplicationSerializer(serializers.ModelSerializer):
    supid=SupplierSerilizer(read_only=True)
    class Meta:
        model=LeaveApplication
        fields="__all__"
        ordering=['-app_date','supid.sup_name',]

class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerilizer(read_only=True)
    class Meta:
        model=UserProfile
        fields='__all__'

class MatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=matgroup
        fields='__all__'
        

class MaterialSerializer(serializers.ModelSerializer):
    #groupid_name = serializers.CharField(source='groupid.name', required=False)
    groupid=MatGroupSerializer(read_only=True)
    groupid_id = serializers.PrimaryKeyRelatedField(queryset=matgroup.objects.all(), source='groupid', write_only=True)
    class Meta:
        model=Material
        fields='__all__'
        ordering=['mat_name']

    def create(self, validated_data):
        print("post")
        groupid_id = validated_data.pop('groupid_id', None)
        if groupid_id:
            group= matgroup.objects.get(pk=groupid_id)
            validated_data['groupid'] = group
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        groupid_id = validated_data.pop('groupid_id', None)
        if groupid_id:
            group= matgroup.objects.get(pk=groupid_id)
            instance.groupid = group
        return super().update(instance, validated_data)

class InventorySerializer(serializers.ModelSerializer):
    supid=SupplierSerilizer(read_only=True)
    supid_id=serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supid', write_only=True)
    matid=MaterialSerializer(read_only=True)
    matid_id=serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), source='matid', write_only=True)
    siteid=SiteSerilizer(read_only=True)
    siteid_id=serializers.PrimaryKeyRelatedField(queryset=Sites.objects.all(), source='siteid', write_only=True)
    class Meta:
        model=Inventory
        fields='__all__'
        ordering=['-ddate']

    def create(self, validated_data):
        print("post")
        supid_id = validated_data.pop('supid_id', None)
        matid_id = validated_data.pop('matid_id', None)
        siteid_id = validated_data.pop('siteid_id', None)
        if supid_id and matid_id and supid_id:
            matid= Material.objects.get(mat_id=matid_id)
            validated_data['matid'] = matid
            supid= Supplier.objects.get(sup_id=supid_id)
            validated_data['supid'] = supid
            siteid= Sites.objects.get(site_id=siteid_id)
            validated_data['siteid'] = siteid
        return super().create(validated_data)
    def update(self, instance, validated_data):
        print("put")
        supid_id = validated_data.pop('supid_id', None)
        matid_id = validated_data.pop('matid_id', None)
        siteid_id = validated_data.pop('siteid_id', None)
        if supid_id and matid_id:
            matid= Material.objects.get(mat_id=matid_id)
            validated_data['matid'] = matid
            supid= Supplier.objects.get(sup_id=supid_id)
            validated_data['supid'] = supid
            siteid= Sites.objects.get(site_id=siteid_id)
            validated_data['siteid'] = siteid
        return super().update(instance, validated_data)
    
class AttTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=AttandanceType
        fields='__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    supid=SupplierSerilizer(read_only=True)
    supid_id=serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supid', write_only=True)
    fhType=AttTypeSerializer(read_only=True)
    fhType_id=serializers.PrimaryKeyRelatedField(queryset=AttandanceType.objects.all(), source='fhType', write_only=True)
    shType=AttTypeSerializer(read_only=True)
    shType_id=serializers.PrimaryKeyRelatedField(queryset=AttandanceType.objects.all(), source='shType', write_only=True)
    class Meta:
        model=Attandance
        fields='__all__'
        