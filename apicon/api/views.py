
from api.models import Sites,Company,Supplier,UserProfile,SalaryRegister,LeaveRegister,LeaveApplication,Material,matgroup,Inventory,Attandance,AttandanceType
from django.contrib.auth.models import User, Group,Permission,AbstractUser
from rest_framework import serializers
from .serilizer import SiteSerilizer,CompanySerilizer,UserSerilizer,GroupSerializer,SupplierSerilizer,SalaryRegisterSerilizer,LeaveRegisterSerializer,LeaveApplicationSerializer,UserProfileSerializer
from .serilizer import MaterialSerializer,MatGroupSerializer,InventorySerializer,AttendanceSerializer,AttTypeSerializer
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
    queryset=LeaveRegister.objects.all().order_by('-ddate')
    serializer_class=LeaveRegisterSerializer
    pagination_class=LeavePageNumberPagination
    
    def list(self,request):
        today = datetime.date.today()
        current_year = today.year
        queryset_current=self.queryset.filter(ddate__year=current_year)
        queryset_old=self.queryset.filter(ddate__year__lte=current_year)
        employees=Supplier.objects.filter(Isactive=1,types="employee").order_by('sup_name').all()
        data=[]
        
        def get_leave_summary(sup_id):
            opbal_casual_result=queryset_old.filter(supid__sup_id=sup_id,lvs_type='casual').aggregate(Sum('leave'))
            opbal_casual = opbal_casual_result['leave__sum'] if opbal_casual_result['leave__sum'] else 0
            opbal_sick_result=queryset_old.filter(supid__sup_id=sup_id,lvs_type='sick').aggregate(Sum('leave'))
            opbal_sick = opbal_sick_result['leave__sum'] if opbal_sick_result['leave__sum'] else 0
            consumed_casual_result=queryset_current.filter(supid__sup_id=sup_id,lvs_type='casual').aggregate(Sum('leave'))
            consumed_casual = consumed_casual_result['leave__sum'] if consumed_casual_result['leave__sum'] else 0
            consumed_sick_result=queryset_current.filter(supid__sup_id=sup_id,lvs_type='sick').aggregate(Sum('leave'))
            consumed_sick = consumed_sick_result['leave__sum'] if consumed_sick_result['leave__sum'] else 0
            leave_summary=[{"leavetype":"casual","opbal":opbal_casual,"consumed":consumed_casual-30},{"leavetype":"sick","opbal":12,"consumed":consumed_sick-12}]
            return leave_summary
        
        for emp in employees:
            name=emp.sup_name
            id=emp.sup_id
            leave_tbl=get_leave_summary(emp.sup_id)
            get_employes={"name":name,"id":id,"year":current_year,"leave":leave_tbl}
            data.append(get_employes)
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=True,methods=['get'])        
    def get_leavebyid(self,request,pk=None):
        queryset_current=self.queryset.filter(supid_id=pk)
        serializer=self.serializer_class(queryset_current,many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True,methods=['get'])        
    def get_leaveapplicationbyid(self,request,pk=None):
        queryset_current=LeaveApplication.objects.filter(supid_id=pk)
        serializer=LeaveApplicationSerializer(queryset_current,many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   
#++++++++++++++++++++++++++++++++++leave application++++++++++++++++++++++++++++++++++++++++++++++++++
class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset=LeaveApplication.objects.all()
    serializer_class=LeaveApplicationSerializer
    pagination_class=CustomPageNumberPagination

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
    queryset=Attandance.objects.all()
    serializer_class=AttendanceSerializer
    pagination_class=CustomPageNumberPagination
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['att_date' ]

class EmployeeList(ListAPIView):   #not in salary register
    queryset = Supplier.objects.filter(types='employee').exclude(suppliers__supid_id__isnull=False)
    serializer_class = SupplierSerilizer

    