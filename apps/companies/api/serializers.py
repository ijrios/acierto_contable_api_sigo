from rest_framework import serializers
from apps.companies.models import Company, Credential

class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nit': instance.nit,
            'business_name': instance.business_name,
            'logo': instance.logo.url if instance.logo else None
        }
        
class CompanySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
    def create(self, validated_data):
        company = Company(**validated_data)
        company.save()
        return company

    def update(self, instance, validated_data):
        instance.nit = validated_data.get('nit', instance.nit)
        instance.business_name = validated_data.get('business_name', instance.business_name)
        instance.save()
        return instance
    
class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'
        
    def create(self, validated_data):
        credential = Credential(**validated_data)
        credential.save()
        return credential

    def update(self, instance, validated_data):
        instance.user_siigo = validated_data.get('user_siigo', instance.user_siigo)
        instance.secret_key_siigo = validated_data.get('secret_key_siigo', instance.secret_key_siigo)
        instance.save()
        return instance

class FileSearchSerializer(serializers.Serializer):
    url = serializers.URLField()