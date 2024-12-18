from companies.views.base import Base
from companies.utils.permission import GroupsPermission
from companies.serializers import PermissionSerializer

from rest_framework.response import Response

from django.contrib.auth.models import permission

class PermissionDetail(Base):
    permission_classes = [GroupsPermission]
    
    def get(self,request):
        permissions = Permission.object.filter(contente_type_id__in=[])