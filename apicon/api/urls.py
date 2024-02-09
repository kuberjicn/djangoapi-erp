from django.urls import path,include
from .views import UserLogIn,UserViewSet,GroupViewSet,LeaveRegisterViewSet,CompanyViewSet,SiteViewSet,SupplierViewSet,SalaryRegisterViewSet
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'leave-register',LeaveRegisterViewSet)
router.register(r'company',CompanyViewSet)
router.register(r'site',SiteViewSet)
router.register(r'entity',SupplierViewSet)
router.register(r'salary-register',SalaryRegisterViewSet)
urlpatterns = router.urls

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#+++++++++++++++++login/permisions url+++++++++++++++++++++++++++++++++++++++++++++++++
    path('api-user-login/', UserLogIn.as_view()),
    #path('permissions/<int:userid>', get_permissions ,name='get_all_permissions'),
#+++++++++++++++++master url+++++++++++++++++++++++++++++++++++++++++++++++++
    #path('company/', get_companys ,name='get_all_company'),
    #path('company/<int:id>', get_company ,name='get_company'),
    # path('site/', get_sites ,name='get_all_sites'),
    # path('site/<int:id>', get_site ,name='get_site'),
    # path('entity/', get_entities ,name='get_all_entities'),
    # path('entity/<int:id>', get_entity ,name='get_entity'),
    # path('salary-registers/', get_salary_registers ,name='get_all_slr'),
    # path('salary-register/<int:id>', get_salary_register ,name='get_slr'),
    
#+++++++++++++++++++++++++++++++++upload++++++++++++++++++++++++++++++++++++++++
   
  
]