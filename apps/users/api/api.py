from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, UserListSerializer, RoleSerializer, RoleListSerializer
from apps.users.models import User, Role
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from accounting_success.mixins import UserRoleMixin

class UserRegisterView(APIView, UserRoleMixin):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(9) # 1.Usuarios all
        
        if serializer.is_valid():
            if permission:
                serializer.save()
                return Response({'message': 'Usuario creado'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView, UserRoleMixin):
    def get(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(9) # 1.Usuarios all
        
        if serializer.is_valid():
            if permission:
                serializer.save()
                return Response({'message': 'Usuario actualizado'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleRegisterView(APIView, UserRoleMixin):
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(10) # 1.Roles all
        
        if serializer.is_valid():
            if permission:
                serializer.save()
                return Response({'message': 'Rol Creado'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoleUpdateView(APIView):
    def put(self, request, pk=None):
        role = get_object_or_404(Role, pk=pk)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(10) # 1.Rol all
        
        if serializer.is_valid():
            if permission:
                serializer.save()
                return Response({'message': 'Rol actualizado'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserActivationView(APIView):
    def post(self, request, pk=None, action=None):
        user = get_object_or_404(User, pk=pk)
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(9) # 1.Usuarios all
        
        if not permission:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if action == 'activate':
                user.is_active = True
                message = 'Usuario Activado'
            elif action == 'deactivate':
                user.is_active = False
                message = 'Usuario Desactivado'
            else:
                return Response({'error': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.save()
            return Response({'message': message}, status=status.HTTP_200_OK)
    
    
class UserListView(generics.ListAPIView, UserRoleMixin):
    def get(self, request):
        user = request.user
        if user.is_staff:
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(9) # 1.Usuarios all
            users = User.objects.all()
            serializer = UserListSerializer(users, many=True)
            if permission:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)
    
class UserListByCompay(generics.ListAPIView, UserRoleMixin):
    def get(self, request, company=None):
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(9) # 1.Usuarios all
        users = User.objects.filter(company=company)
        serializer = UserListSerializer(users, many=True)
        if permission:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)

class RolListView(generics.ListAPIView):
    def get(self, request):
        user = request.user
        if user.is_staff:
            mixin = UserRoleMixin(request)
            permission = mixin.check_permissions(10) # 1.Roles all
            roles = Role.objects.all()
            serializer = RoleListSerializer(roles, many=True)
            if permission:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_403_FORBIDDEN)

class RoleListByCompany(generics.ListAPIView, UserRoleMixin):
    def get(self, request, company=None):
        mixin = UserRoleMixin(request)
        permission = mixin.check_permissions(10) # 1.Roles all
        roles = Role.objects.filter(company=company)
        serializer = RoleListSerializer(roles, many=True)
        if permission:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No tiene permisos para realizar esta acción'}, status=status.HTTP_400_BAD_REQUEST)