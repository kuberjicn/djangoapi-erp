from django.urls import path,include
from .views import UserLogIn,UserViewSet,GroupViewSet,LeaveRegisterViewSet,CompanyViewSet,SiteViewSet,SupplierViewSet,SalaryRegisterViewSet,LeaveApplicationViewSet,UserProfileViewSet,MaterialViewSet,MaterialGroupViewSet,EmployeeList
from .views import InventoryViewSet,AttendanceViewSet,AttTypeViewSet
from django.contrib import admin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'leave-register',LeaveRegisterViewSet)
router.register(r'company',CompanyViewSet)
router.register(r'site',SiteViewSet)
router.register(r'entity',SupplierViewSet)
router.register(r'salary-register',SalaryRegisterViewSet)
router.register(r'leave-register',LeaveRegisterViewSet)
router.register(r'leave-application',LeaveApplicationViewSet)
router.register(r'user-profile',UserProfileViewSet)
router.register(r'material-group',MaterialGroupViewSet)
router.register(r'material',MaterialViewSet)
router.register(r'inventory',InventoryViewSet)
router.register(r'att-type',AttTypeViewSet)
router.register(r'attendance',AttendanceViewSet)


urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
   
#+++++++++++++++++login/permisions url+++++++++++++++++++++++++++++++++++++++++++++++++
    path('api-user-login/', UserLogIn.as_view(),name='login'),
#+++++++++++++++++++get employe that not exist in salary register +++++++++++++++++++
    path('no-employee/', EmployeeList.as_view(), name='no_employee'),
 ]