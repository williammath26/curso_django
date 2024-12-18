from django.urls import path

from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups ,GroupDetail
from companies.views.tasks import Tasks,TaskDetail

urlpatterns = [
    # Lista de funcionários
    path('employees', Employees.as_view(), name='employees_list'),
    # Detalhes de um funcionário
    path('employees/<int:employee_id>', EmployeeDetail.as_view(), name='employee_detail'),
    
    #Groups anda permissions anda endpoins
    path('groups', Groups.as_view(), name='group_list'),  # Para listar os grupos
    path('groups/<int:group_id>', GroupDetail.as_view(), name='group_detail'),  # Para acessar um grupo específico
    path('permissions',PermissionDetail.as_view()),

    #tasks endpoints

    path('tasks',Tasks.as_view()),
    path('tasks/<int:task_id>',TaskDetail.as_view())
]
