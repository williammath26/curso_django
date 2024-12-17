from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from accounts.models import User_Grups , Group_Permissions
from companies.models import Enterprise , Employee

class Base(APIView):
    def get_enterpprise_user(self,user_id):
        enterprise = {
            "is_owner":False,
            "permissions":[]
        }
        enterprise['is_owner'] = Enterprise.objects.filter(user_id=user_id).exists()
        
        if enterprise['is_owner']: return enterprise
        
        #permissions,get employee
        employee = Employee.objects.filter(user_id = user_id).first()
        
        if not employee:
            raise APIException("Este usuário não é um funcionário")
        
        groups = User_Grups.objects.filter(user_id=user_id).all()
        
        for g in groups:
            group = g.group
            
            permissions = Group_Permissions.objects.filter(goup_id=group.id).all()
            
            for p in permissions:
                enterprise['permissions'].append({
                    "id": p.permission.id,
                    "label":p.permission.name,
                    "codename":p.permission.codename
                })
                
            return enterprise