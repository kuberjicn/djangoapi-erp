from api.models import Sites,Company,Supplier,UserProfile,SalaryRegister,LeaveRegister
from django.contrib.auth.models import User, Group,Permission,AbstractUser
from rest_framework import serializers
from .serilizer import SiteSerilizer,CompanySerilizer,UserSerilizer,GroupSerializer,SupplierSerilizer,SalaryRegisterSerilizer,LeaveRegisterSerializer
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
# class UserPermission(viewsets.ModelViewSet):
#     def get_permissions(self):
#         user = self.request.user
#         codenames = user.user_permissions.values_list('codename', flat=True)
#         codenames_list = list(codenames)
        
#         class CustomPermission(BasePermission):
#             def has_permission(self, request, view):
#                 # Check if the user has any of the required permissions
#                 return any(permission in codenames_list for permission in 'add_user')
        
#         return [CustomPermission()]



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
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[TokenAuthentication]

    def list(self, request):
        filter_value = request.GET.get('filter2')
        if filter_value is None or filter_value == '':
            queryset = self.queryset.all()
        else:
            queryset = self.queryset.filter(types=filter_value)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            adharphoto_file = request.data.get('adharphoto', None)
            photo_file = request.data.get('photo', None)
            if adharphoto_file and not isinstance(adharphoto_file, str):
                instance.adharphoto.save(adharphoto_file.name, adharphoto_file)
            if photo_file and not isinstance(photo_file, str):
                instance.photo.save(photo_file.name, photo_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

#+++++++++++++++++++++++++++++salary register+++++++++++++++++++++++++++

class SalaryRegisterViewSet(viewsets.ModelViewSet):
    queryset=SalaryRegister.objects.filter(deleted=0).all().order_by('supid__sup_name')
    serializer_class=SalaryRegisterSerilizer
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            oldsalid = request.data.get('oldsal_id', None)
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



class LeaveRegisterViewSet(viewsets.ModelViewSet):
    queryset=LeaveRegister.objects.all().order_by('-ddate')
    serializer_class=LeaveRegisterSerializer
    #permission_classes= [permissions.DjangoModelPermissions]
    # authentication_classes=[TokenAuthentication]



