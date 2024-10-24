from django.db import models
from accounting_success.base_model import BaseModel

def default_logo():
    return 'logos_empresas/default.png'

class Company(BaseModel):
    nit = models.CharField(max_length=255, unique=True, verbose_name='NIT')
    business_name = models.CharField(max_length=255, verbose_name='Razón Social')
    logo = models.ImageField(upload_to='logos_empresas/', default=default_logo, verbose_name='Logo', null=True, blank=True)
    
    class Meta:
        db_table = 'empresas'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return f"{self.business_name} - {self.nit}"

class Credential(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Empresa')
    user_siigo = models.CharField(max_length=255, verbose_name='Usuario Siigo')
    secret_key_siigo = models.CharField(max_length=255, verbose_name='Clave Siigo')
    
    class Meta:
        db_table = 'credenciales'
        verbose_name = 'Credencial'
        verbose_name_plural = 'Credenciales'

    def __str__(self):
        return self.company.business_name