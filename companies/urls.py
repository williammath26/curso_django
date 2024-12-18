from django.urls import path

from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail

urlpatterns = [
    # Lista de funcionários
    path('employees', Employees.as_view(), name='employees_list'),
    # Detalhes de um funcionário
    path('employees/<int:employee_id>', EmployeeDetail.as_view(), name='employee_detail'),
    
    #Groups anda permissions anda endpoins
    path('permissions',PermissionDetail.as_view())
]
