
from api.models import Sites,Company,Supplier,UserProfile,SalaryRegister,LeaveRegister,LeaveApplication,Material,matgroup,Inventory,Attandance,AttandanceType,PayrollList,DetailPayroll
from django.contrib.auth.models import User, Group,Permission,AbstractUser
from rest_framework import serializers
from .serilizer import SiteSerilizer,CompanySerilizer,UserSerilizer,GroupSerializer,SupplierSerilizer,SalaryRegisterSerilizer,LeaveRegisterSerializer,LeaveApplicationSerializer,UserProfileSerializer
from .serilizer import MaterialSerializer,MatGroupSerializer,InventorySerializer,AttendanceSerializer,AttTypeSerializer,PayRollListSerializer,DetailPayRollSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import BasePermission
import json
from django_filters.rest_framework import DjangoFilterBackend
from api.myPgination import CustomPageNumberPagination,LeavePageNumberPagination
from django.views.generic import ListView 
from rest_framework.generics import ListAPIView
from django.core.files.base import ContentFile
import os
from django.forms.models import model_to_dict
from rest_framework.decorators import action
import datetime
from django.db.models import Sum
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from datetime import  timedelta
#-----------------------------user data and login--------------------------------------------
class UserLogIn(ObtainAuthToken):
    authentication_classes=[BasicAuthentication]
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user2 = User.objects.get(pk=user.pk)
        token,created = Token.objects.get_or_create(user=user)
        pic=UserProfile.objects.get(user=user)
        if user2.is_superuser :
            codenames = Permission.objects.values_list('codename', flat=True)
        else:
            codenames = user2.user_permissions.values_list('codename', flat=True)
       
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username,
            'firstname':user.first_name.strip(),
            'pic':pic.profile_picture.url,
            'codename': codenames
        })
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_permissions(request,userid):
        #print(request)
        user = User.objects.get(pk=userid)
        codenames = user.user_permissions.values_list('codename', flat=True)
        codenames_list = list(codenames)
        codenames_json = json.dumps(codenames_list)
        return Response({'codenames': codenames_list})



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerilizer
    # permission_classes = [permissions.IsAuthenticated]
   
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]

# -----------------company-------------------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset=Company.objects.all().order_by('compname')
    serializer_class=CompanySerilizer
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[TokenAuthentication]
   


# -----------------site-------------------------------------
    
class SiteViewSet(viewsets.ModelViewSet):
    queryset=Sites.objects.all().order_by('sitename') 
    serializer_class=SiteSerilizer
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[TokenAuthentication]

    

        
# -----------------entity-------------------------------------
    

class SupplierViewSet(viewsets.ModelViewSet):
    queryset=Supplier.objects.all().order_by('sup_name') 
    serializer_class=SupplierSerilizer
    pagination_class=CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['types']
    
    # def list(self, request):
    #     filter_value = request.GET.get('filter2')
    #     if filter_value is None or filter_value == '':
    #         queryset = self.queryset.all()
    #     else:
    #         queryset = self.queryset.filter(types=filter_value)
    #     paginated_queryset = self.paginate_queryset(queryset)
    #     serializer = self.serializer_class(paginated_queryset, many=True)
    #     return self.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            adharphoto_file = request.data.get('adharphoto', None)
            photo_file = request.data.get('photo', None)
            if adharphoto_file and not isinstance(adharphoto_file, str):
                instance.adharphoto.save(adharphoto_file.name, adharphoto_file)
            if photo_file and not isinstance(photo_file, str):
                instance.photo.save(photo_file.name, photo_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
       #print(self.as_view)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            adharphoto_file = request.data.get('adharphoto', None)
            print(adharphoto_file)
            if adharphoto_file and not isinstance(adharphoto_file, str):
                if not os.path.exists(adharphoto_file.name):
                    instance.adharphoto.save(adharphoto_file.name, adharphoto_file)
            photo_file = request.data.get('photo', None)
            if photo_file and not isinstance(photo_file, str):
                if not os.path.exists(photo_file.name):
                    instance.photo.save(photo_file.name, photo_file)
            print(adharphoto_file,photo_file)
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

#+++++++++++++++++++++++++++++salary register+++++++++++++++++++++++++++

class SalaryRegisterViewSet(viewsets.ModelViewSet):
    queryset=SalaryRegister.objects.filter(deleted=False)
    serializer_class=SalaryRegisterSerilizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['supid__Isactive']
    
    def update(self, request, pk=None):
        serilizer=self.serializer_class(data=request.data)
        sr_instance=SalaryRegister.objects.get(sal_id=pk)
        #inst_serilizer=self.serializer_class(instance= sr_instance ,data='request.data')
        if serilizer.is_valid():
            sr_instance.deleted=True
            sr_instance.save()
            sr=serilizer.save()
            return Response({'msg':'data updated successfully'}, status=status.HTTP_201_CREATED)
        return Response({'msg':'something got wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['post'])
    def resign(self,request,pk=None):
        #print(pk)
        sal_instance=SalaryRegister.objects.get(sal_id=pk)
        supid_id=sal_instance.supid.sup_id
        #sal_instance.deleted=True
        if supid_id:
            #data={'supid':supid_id}
            sup=Supplier.objects.get(sup_id=supid_id)
            sup.Isactive=False
            sup.save()
            #sal_instance.save()
            return Response({'msg':'employee resigned'}, status=status.HTTP_201_CREATED)
        return Response({'msg':'something got wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['post'])
    def rejoin(self,request,pk=None):
        #print(pk)
        sal_instance=SalaryRegister.objects.get(sal_id=pk)
        supid_id=sal_instance.supid.sup_id
        #sal_instance.deleted=True
        if supid_id:
            #data={'supid':supid_id}
            sup=Supplier.objects.get(sup_id=supid_id)
            sup.Isactive=True
            sup.save()
            #sal_instance.save()
            return Response({'msg':'employee rejoined'}, status=status.HTTP_201_CREATED)
        return Response({'msg':'something got wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True,methods=['get'])
    def history(self,request,pk=None):
        #print(pk)
        supid_id=SalaryRegister.objects.get(sal_id=pk).supid_id
        if supid_id:
            #data={'supid':supid_id}
            salary_registers=SalaryRegister.objects.filter(supid_id=supid_id).order_by('-sal_id')
            serializer=self.serializer_class(salary_registers,many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg':'something got wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    


#+++++++++++++++++++++++++++++++++++++++leave register+++++++++++++++++++++++++++++++++++++++++++++++
class LeaveRegisterViewSet(viewsets.ModelViewSet):
    queryset=LeaveRegister.objects.order_by('-ddate')
    serializer_class=LeaveRegisterSerializer
    pagination_class=CustomPageNumberPagination
    
    def list(self,request):
        today = datetime.date.today()
        current_year = today.year
        years= request.GET.get('year')
        if years is not None and years.strip():
            current_year=str(years)
 
        queryset_current=self.queryset.filter(ddate__year=current_year)
        queryset_old=self.queryset.filter(ddate__year__lt=current_year)
        employees=Supplier.objects.filter(Isactive=1,types="employee").order_by('sup_name').all()
        data=[]
        
        def get_leave_summary(sup_id):
            opbal_casual_result=queryset_old.filter(supid__sup_id=sup_id,lvs_type='casual').aggregate(Sum('leave'))
            past_opbal_casual = opbal_casual_result['leave__sum'] if opbal_casual_result['leave__sum'] else 0 #past year casual balance
            
            current_opbal_casual_result=queryset_current.filter(supid__sup_id=sup_id,lvs_type='casual',leave__gt=0).aggregate(Sum('leave'))
            current_opbal = current_opbal_casual_result['leave__sum'] if current_opbal_casual_result['leave__sum'] else 0 #current year added leave sum
            
            current_casual_consumed_result=queryset_current.filter(supid__sup_id=sup_id,lvs_type='casual',leave__lt=0).aggregate(Sum('leave'))
            current_casual_consumed = current_casual_consumed_result['leave__sum'] if current_casual_consumed_result['leave__sum'] else 0 # current year consumed sum
            
            consumed_sick_result=queryset_current.filter(supid__sup_id=sup_id,lvs_type='sick',leave__lt=0).aggregate(Sum('leave'))
            consumed_sick = consumed_sick_result['leave__sum'] if consumed_sick_result['leave__sum'] else 0 #current year sick consumed sum
            leave_summary=[{"leavetype":"casual","opbal":past_opbal_casual+current_opbal,"consumed":current_casual_consumed},{"leavetype":"sick","opbal":12,"consumed":consumed_sick}] #json formation
            return leave_summary
        for emp in employees:
            name=emp.sup_name
            id=emp.sup_id
            leave_tbl=get_leave_summary(emp.sup_id) # get data in json of leave
            #print(leave_tbl)
            get_employes={"name":name,"id":id,"year":current_year,"leave":leave_tbl}
            data.append(get_employes)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=True,methods=['get'])        
    def get_leavebyid(self,request,pk=None):
        supobj=Supplier.objects.get(sup_id=pk)
        print(supobj)
        queryset_current=self.queryset.filter(supid_id=pk)
        today = datetime.date.today()
        current_year = today.year
        years= request.GET.get('year')
        if years is not None and years.strip():
            current_year=str(years)

        stdate=str(current_year)+'-01-01'
        opbal_casual_result=queryset_current.filter(lvs_type='casual',ddate__year__lt=current_year).aggregate(Sum('leave'))
        past_opbal_casual = opbal_casual_result['leave__sum'] if opbal_casual_result['leave__sum'] else 0 #past year casual balance
        
        clbal_casual_result=queryset_current.filter(lvs_type='casual',ddate__year__lte=current_year).aggregate(Sum('leave'))
        clbal_casual = clbal_casual_result['leave__sum'] if clbal_casual_result['leave__sum'] else 0 #past year casual balance

# casual query set----------------------------------------
        casulat_queryset=queryset_current.filter(ddate__year=current_year,lvs_type='casual').order_by('ddate')
        firstrow={'lvr_id':'','ddate':'','leave':past_opbal_casual,'lvs_type':'','la_app_id':'','disp':'Oening Balance'}
        lastrow={'lvr_id':'','ddate':'Panding Leave','leave':clbal_casual,'lvs_type':'','la_app_id':'','disp':'Closing Balance'}
        serializer=self.serializer_class(casulat_queryset,many=True)
        casual_data = [firstrow] + serializer.data + [lastrow]
# sick query set
        sick_queryset=queryset_current.filter(ddate__year=current_year,lvs_type='sick').order_by('ddate')
        firstrow1={'lvr_id':'','ddate':'','leave':0,'lvs_type':'','la_app_id':'','disp':'Oening Balance'}
        lastrow1={'lvr_id':'','ddate':'Panding Leave','leave':12,'lvs_type':'','la_app_id':'','disp':'Closing Balance'}
        serializer1=self.serializer_class(sick_queryset,many=True)
        sick_data = [firstrow1] + serializer1.data + [lastrow1]

        postdata={"casualdata":casual_data,"sickdata":sick_data,"empid":pk,'supname':supobj.sup_name}
        
        return Response(postdata, status=status.HTTP_201_CREATED)
    
    @action(detail=True,methods=['get'])        
    def get_leaveapplicationbyid(self,request,pk=None):
        today = datetime.date.today()
        current_year = today.year
        years= request.GET.get('year')
        print('year',years)
        if years is not None and years.strip():
            current_year=str(years)
        supobj=Supplier.objects.get(sup_id=pk)
        queryset_casual=LeaveApplication.objects.filter(supid_id=pk ,from_date__year=current_year,isapproved=True)
        serializer_casual=LeaveApplicationSerializer(queryset_casual,many=True)
        
        postdata={'casual':serializer_casual.data,'supname':supobj.sup_name,'supid':supobj.sup_id}
        
        return Response(postdata, status=status.HTTP_201_CREATED)
   
#++++++++++++++++++++++++++++++++++leave application++++++++++++++++++++++++++++++++++++++++++++++++++
class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset=LeaveApplication.objects.order_by('-app_date')
    serializer_class=LeaveApplicationSerializer
    pagination_class=CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['isapproved']
    
    def partial_update(self,request,pk=None):
        approve=request.data.get('isapproved')
        app_instance=LeaveApplication.objects.get(app_id=pk)
        app_instance.isapproved=approve
        leave_days=app_instance.nosDays
        from_date=app_instance.from_date
        leave_type=app_instance.lvs_type
        section=app_instance.section
        supid=app_instance.supid.sup_id
        nosdays=int(app_instance.nosDays)
        if approve:
            if leave_type=='casual':
                lvsid=4
            else:
                lvsid=5
        else:
            lvsid=2
        
        if section == 'both':
            to_date=from_date + timedelta(days=nosdays)
            for i in range(nosdays):
                att_instance={
                    'att_date':from_date + timedelta(days=i),
                    'supid_id':supid,
                    'username':'sys',
                    'fhType_id':lvsid,
                    'shType_id':lvsid,
                    'intime':'00:00:00',
                    'outtime':'00:00:00',
                }
                Attandance.objects.update_or_create(att_date=att_instance['att_date'],supid_id=supid,defaults=att_instance)
        elif section=='sh':
            att_instance={
                    'att_date':from_date,
                    'supid_id':supid,
                    'username':'sys',
                    'shType_id':lvsid,
                    'intime':'08:00:00',
                    'outtime':'13:00:00',
                }
            to_date=from_date
            Attandance.objects.update_or_create(att_date=from_date,supid_id=supid, defaults=att_instance)
        elif section=='fh':
            att_instance={
                    'att_date':from_date,
                    'supid_id':supid,
                    'username':'sys',
                    'fhType_id':lvsid,
                    'intime':'14:00:00',
                    'outtime':'19:00:00',
                }
            to_date=from_date
            Attandance.objects.update_or_create(att_date=from_date,supid_id=supid, defaults=att_instance)
        if approve:
            leave_register_istance={
                'ddate':from_date,
                'leave':leave_days *-1 ,
                'lvs_type':leave_type,
                'supid_id':supid,
                'la_app_id':pk,
                'disp':f"{leave_days} day/days leave granted from {from_date} to {to_date}"
            }
            LeaveRegister.objects.update_or_create(la_app_id=leave_register_istance['la_app_id'], defaults=leave_register_istance)
        else:
            LeaveRegister.objects.filter(la_app_id=pk).delete()
        app_instance.save()
        return Response({'msg':'data updated successfully'}, status=status.HTTP_201_CREATED) 

#++++++++++++++++++++++++++++++++++ userprofile application++++++++++++++++++++++++++++++++++++++++++++++++++ 
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer

#++++++++++++++++++++++++++++++++++ material group ++++++++++++++++++++++++++++++++++++++++++++++++++ 
class MaterialGroupViewSet(viewsets.ModelViewSet):
    queryset=matgroup.objects.all()
    serializer_class=MatGroupSerializer

#++++++++++++++++++++++++++++++++++ material ++++++++++++++++++++++++++++++++++++++++++++++++++ 
class MaterialViewSet(viewsets.ModelViewSet):
    queryset=Material.objects.all()
    serializer_class=MaterialSerializer
    pagination_class=CustomPageNumberPagination

#++++++++++++++++++++++++++++++++++ Inventory ++++++++++++++++++++++++++++++++++++++++++++++++++ 
class InventoryViewSet(viewsets.ModelViewSet):
    queryset=Inventory.objects.all()
    serializer_class=InventorySerializer
    pagination_class=CustomPageNumberPagination

#++++++++++++++++++++++++++++++++++ attandance type ++++++++++++++++++++++++++++++++++++++++++++++++++ 
class AttTypeViewSet(viewsets.ModelViewSet):
    queryset=AttandanceType.objects.all()
    serializer_class=AttTypeSerializer

#++++++++++++++++++++++++++++++++++ attandance  ++++++++++++++++++++++++++++++++++++++++++++++++++ 
    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset=Attandance.objects.filter(supid__Isactive=True).order_by('supid__sup_name').all()
    serializer_class=AttendanceSerializer
    pagination_class=CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['att_date' ]

    def partial_update(self,request,pk=None):
        qset=Attandance.objects.get(att_id=pk)
        data=request.data
        intime='08:00:00'
        outtime='19:00:00'
        
            
        if 'fhType_id' in data:
            newfhtype=data['fhType_id']
            print(qset.shType_id,newfhtype)
            if qset.shType_id==2 and newfhtype==2:
                qset.intime='00:00:00'
                qset.outtime='00:00:00'
            if qset.shType_id==3 and newfhtype==3:
                qset.intime=intime
                qset.outtime=outtime
            if qset.shType_id==2 and newfhtype==3:
                qset.intime=intime
                qset.outtime='13:00:00'
            if qset.shType_id==3 and newfhtype==2:
                qset.intime='14:00:00'
                qset.outtime=outtime
            qset.fhType_id=newfhtype
            

        if'shType_id' in data:
            newshtype=data['shType_id']
            print(qset.fhType_id,newshtype)
            if qset.fhType_id==2 and newshtype==2:
                qset.intime='00:00:00'
                qset.outtime='00:00:00'
            if qset.fhType_id==3 and newshtype==3:
                qset.intime=intime
                qset.outtime=outtime
            if qset.fhType_id==2 and newshtype==3:
                qset.intime='14:00:00'
                qset.outtime=outtime
            if qset.fhType_id==3 and newshtype==2:
                qset.intime=intime
                qset.outtime='13:00:00'
            qset.shType_id=newshtype
        qset.save()
        #print(data['shType_id'])
        return Response({'msg':'data updated successfully'}, status=status.HTTP_201_CREATED)
        #return Response({'msg':'something got wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['post'])
    def makeAllpresent(self,request,pk=None):
        ddate= request.GET.get('att_date')
        print(ddate)
        newqueryset=self.queryset.filter(att_date=ddate)
        for emp in newqueryset:
            if emp.fhType_id==2:
                emp.fhType_id=3
            if emp.shType_id==2:
                emp.shType_id=3
            emp.intime='08:00:00'
            emp.outtime='19:00:00'
            emp.save()
        return Response({'msg':'employee presented'}, status=status.HTTP_201_CREATED)
    #return Response({'msg':'something got wrong'}, status=status.HTTP_400_BAD_REQUEST)
#------------------------------------------custom url---------------------------------------------------
class EmployeeList(ListAPIView):   #not in salary register
    queryset = Supplier.objects.filter(types='employee').exclude(suppliers__supid_id__isnull=False)
    serializer_class = SupplierSerilizer


 
def YearList(request):
    distinct_years = LeaveRegister.objects.annotate(year=ExtractYear('ddate')).values('year').distinct()
    years_list = [entry['year'] for entry in distinct_years]
    dist_year_list=list(set(years_list))
    print(dist_year_list)
    return JsonResponse({'years': dist_year_list}, status=status.HTTP_200_OK)
   
#+++++++++++++++++++++++++++++++++++++++++payrol+++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PayrollListViewSet(viewsets.ModelViewSet):
    queryset=PayrollList.objects.all().order_by('st_date') 
    serializer_class=PayRollListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['st_date__year' ]

class DetailPayRillViewSet(viewsets.ModelViewSet):
    queryset=DetailPayroll.objects.all().order_by('supid__sup_name') 
    serializer_class=DetailPayRollSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Plsid_id' ]