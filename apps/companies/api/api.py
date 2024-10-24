from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from apps.companies.models import Company, Credential
from apps.companies.api.serializers import CompanyListSerializer, CompanySerilizer, CredentialSerializer, FileSearchSerializer
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from accounting_success.mixins import UserRoleMixin
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, RoleSerializer

class CompanyList(generics.ListAPIView,UserRoleMixin):
    def get(self, request):
        user = request.user
        if user.is_staff:
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(11) # 1.Company all
            if permission:
                companies = Company.objects.all()
                serializer = CompanyListSerializer(companies, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:   
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

class CompanyCreate(APIView, UserRoleMixin):
    def create_user_default(self, company, role):
        username = 'admin_' + company.business_name.lower().replace(' ', '_')
        password = company.business_name
        email = f'admin@{company.business_name.lower().replace(" ", "")}.com'
        
        user = {
            'username': username,
            'email': email,
            'first_name': 'Admin',
            'last_name': company.business_name,
            'password': password,
            'company': company.id,
            'document': company.nit,
            'role': role.id
        }
        
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            serializer.save()
            return {'status': True}
        else:
            return {'status': False, 'errors': serializer.errors}
    
    def create_role_default(self, company):
        role_data = {
            'name': 'general_admin',
            'description': 'Rol administrador general',
            'permissions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'company': company.id
        }
        
        serializer = RoleSerializer(data=role_data)
        if serializer.is_valid():
            serializer.save()
            return {'status': True}
        else:
            return {'status': False, 'errors': serializer.errors}
        
    def post(self, request):
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(11) # 1.Company all
        serializer = CompanySerilizer(data=request.data)
        if serializer.is_valid():
            if permission:
                company = serializer.save()
                role = self.create_role_default(company)
                
                if role:  
                    user_creation_result = self.create_user_default(company, role)
                    
                    if user_creation_result['status']:
                        return Response({'message': 'Compañía creada y usuario por defecto creados'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'message': 'Compañía creada, pero falló la creación del usuario por defecto', 'errors': user_creation_result['errors']}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Compañía creada, pero falló la creación del rol por defecto'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyUpdate(APIView, UserRoleMixin):
    def get(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerilizer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerilizer(company, data=request.data, partial=True)
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(11) # 1.Company all
        if serializer.is_valid():
            if permission:
                serializer.save()
                return Response({'message': 'Company updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyActivate(APIView, UserRoleMixin):
    def post(self, request, pk=None, action=None):
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(11) # 1.Company all
        company = get_object_or_404(Company, pk=pk)
        
        if permission:
            if action == 'activate':
                company.is_active = True
                message = 'Company activated'
            elif action == 'deactivate':
                company.is_active = False
                message = 'Company deactivated'
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
            
            company.save()
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
      
    
class CredentialCreate(APIView, UserRoleMixin):
    def post(self, request):
        serializer = CredentialSerializer(data=request.data)
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(11) # 1.Company all
        if serializer.is_valid():
            if permission: 
                serializer.save()
                return Response({'message': 'Credential created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CredentialUpdate(APIView, UserRoleMixin):
    def get(self, request, pk=None):
        credential = get_object_or_404(Credential, pk=pk)
        serializer = CredentialSerializer(credential)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(11) # 1.Company all
        credential = get_object_or_404(Credential, pk=pk)
        serializer = CredentialSerializer(credential, data=request.data, partial=True)
        if serializer.is_valid():
            if permission:
                serializer.save()
                return Response({'message': 'Credential updated'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MediaFileView(APIView, UserRoleMixin):
    def get(self, request):
        file_path = request.query_params.get('file_path', '')
        file_full_path = os.path.join(settings.BASE_DIR, file_path)
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(11) # 1.Company all
        
        if permission:
            if os.path.exists(file_full_path):
                return FileResponse(open(file_full_path, 'rb'))
            else:
                return Response(
                    {"error": "File not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
    
