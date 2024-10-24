from rest_framework import serializers
from apps.users.models import User, Role
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
import json 

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'document', 'email', 'first_name', 'last_name', 'company', 'role']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.document = validated_data.get('document', instance.document)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.company = validated_data.get('company', instance.company)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.role = validated_data.get('role', instance.role)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
class RoleSerializer(serializers.ModelSerializer):
    
    permissions = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=8),
        write_only=True
    )
    
    class Meta:
        model = Role
        fields = '__all__'
        
    def validate_permissions(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("El campo 'permissions' debe ser una lista.")
        
        if not all(isinstance(item, int) and 1 <= item <= 8 for item in value):
            raise serializers.ValidationError("El campo 'permissions' debe contener solo números del 1 al 8.")
        
        return value
    
    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        validated_data['permissions'] = json.dumps(permissions)
        role = Role(**validated_data)
        role.save()
        return role
    
    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        if permissions is not None:
            validated_data['permissions'] = json.dumps(permissions)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.permissions = validated_data.get('permissions', instance.permissions)
        instance.save()
        return instance
    
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'document': instance.document,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'company': instance.company.business_name if instance.company else None,
            'role': instance.role.name if instance.role else None,  
            'is_active': instance.is_active,
        }
        
class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'permissions': instance.permissions,
        }
        