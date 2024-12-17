from companies.views.base import Base
from companies.utils.permissions import EmployeesPermission
from companies.models import Employee, Enterprise
from companies.serializers import EmployeeSerializer
from accounts.auth import Authentication
from accounts.models import User, User_Grups
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException


class Employees(Base):
    permission_classes = [EmployeesPermission]

    def get(self, request):
        """
        Lista os funcionários de uma empresa, exceto o dono.
        """
        enterprise_id = self.get_enterprise_id(request.user.id)

        # Obtém o dono da empresa
        owner = Enterprise.objects.filter(id=enterprise_id).values('user_id').first()
        if not owner:
            raise APIException("Empresa não encontrada.", code="enterprise_not_found")

        owner_id = owner['user_id']

        # Busca funcionários, exceto o dono
        employees = Employee.objects.filter(enterprise_id=enterprise_id).exclude(user_id=owner_id)
        serializer = EmployeeSerializer(employees, many=True)

        return Response({"employees": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Cria um novo funcionário.
        """
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        # Valida os campos obrigatórios
        if not all([name, email, password]):
            return Response(
                {"error": "Nome, email e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        enterprise_id = self.get_enterprise_id(request.user.id)

        try:
            # Tenta criar o usuário
            signup_user = Authentication().signup(
                name=name,
                email=email,
                password=password,
                type_account='employee',  # ou 'owner' dependendo do caso
                company_id=enterprise_id  # Se for um funcionário, a empresa precisa ser fornecida
            )
            if isinstance(signup_user, User):
                return Response({'success': True}, status=status.HTTP_201_CREATED)  # Código 201 para criação bem-sucedida
            else:
                return Response({'error': signup_user['error']}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            # Captura erros inesperados
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmployeeDetail(Base):
    permission_classes = [EmployeesPermission]

    def get(self, request, employee_id):
        """
        Obtém os detalhes de um funcionário.
        """
        employee = self.get_employee(employee_id, request.user.id)
        if not employee:
            raise APIException("Funcionário não encontrado.", code="employee_not_found")

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, employee_id):
        """
        Atualiza os dados de um funcionário.
        """
        groups = request.data.get('groups')

        employee = self.get_employee(employee_id, request.user.id)
        if not employee:
            raise APIException("Funcionário não encontrado.", code="employee_not_found")

        # Atualiza nome e email
        name = request.data.get('name') or employee.user.name
        email = request.data.get('email') or employee.user.email

        if email != employee.user.email and User.objects.filter(email=email).exists():
            raise APIException("Esse email já está em uso.", code="email_already_use")

        # Atualiza os dados do usuário
        User.objects.filter(id=employee.user.id).update(name=name, email=email)

        # Atualiza os grupos do funcionário
        User_Grups.objects.filter(user_id=employee.user.id).delete()

        if groups:
            group_ids = groups.split(',')
            for group_id in group_ids:
                self.get_group(group_id, employee.enterprise.id)
                User_Grups.objects.create(group_id=group_id, user_id=employee.user.id)

        return Response({"success": True}, status=status.HTTP_200_OK)

    def delete(self, request, employee_id):
        """
        Deleta um funcionário, mas não o dono da empresa.
        """
        employee = self.get_employee(employee_id, request.user.id)
        if not employee:
            raise APIException("Funcionário não encontrado.", code="employee_not_found")

        # Verifica se o funcionário é o dono
        if User.objects.filter(id=employee.user.id, is_owner=True).exists():
            raise APIException("Você não pode demitir o dono da empresa.", code="owner_cannot_be_deleted")

        # Deleta o funcionário e o usuário associado
        employee.delete()
        User.objects.filter(id=employee.user.id).delete()

        return Response({"success": True}, status=status.HTTP_200_OK)
