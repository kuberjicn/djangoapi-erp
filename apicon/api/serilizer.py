
from  api.models import Sites,Company,Supplier,SalaryRegister,LeaveRegister
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class CompanySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields ='__all__' 
   

class SiteSerilizer(serializers.ModelSerializer):
    
    compid=CompanySerilizer()
    class Meta:
        model = Sites
        fields ='__all__' 
        

    def create(self, validated_data):
         compid_data = validated_data.pop('compid', {})
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
    supid=SupplierSerilizer()
    class Meta:
        model = SalaryRegister
        fields ='__all__' 

class LeaveRegisterSerializer(serializers.ModelSerializer):
    supid=SupplierSerilizer()
    class Meta:
        model=LeaveRegister
        fields="__all__"
        