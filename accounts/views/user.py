
from accounts.views.base import Base
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserSerializers
from rest_framework.response import Response

class GetUser(Base):
    parmission_classes = [IsAuthenticated]
    
    def get(self , request)->None:
        user =User.objects.filter(id = request.user.id).first()
        enterprise = self.get_enterpprise_user(user)
        
        serializer = UserSerializers(user)
        
        return Response ({
            "user":serializer.data,
            'enterprise': enterprise
        })