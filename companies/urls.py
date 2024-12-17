from django.urls import path

from companies.views.employees import Employees, EmployeeDetail

urlpatterns = [
    #employees endpoints
    path('employees', Employees.as_view()),
    path('Employees/<int:employee_id>',EmployeeDetail.as_view())
    
    
]
