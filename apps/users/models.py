from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from apps.companies.models import Company
from accounting_success.base_model import BaseModel

class UserManager(BaseUserManager):
    def _create_user(self, username, email, first_name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, first_name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, first_name,last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name,last_name, password, True, True, **extra_fields)

class Role(BaseModel):
    name = models.CharField(max_length = 255, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    permissions = models.JSONField(verbose_name='Permisos')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 255, unique = True, verbose_name='Nombre de Usuario')
    document = models.CharField(max_length = 255, verbose_name='Documento de Identidad', null=True, blank=True)
    email = models.EmailField(max_length = 255, unique = True, verbose_name='Correo Electrónico')
    first_name = models.CharField(max_length = 255, blank = True, null = True, verbose_name='Nombres')
    last_name = models.CharField(max_length = 255, blank = True, null = True, verbose_name='Apellidos')
    image = models.ImageField(upload_to='perfil/', max_length=255, null=True, blank = True, verbose_name='Imagen de Perfil')
    is_active = models.BooleanField(default = True, verbose_name='Activo')
    is_staff = models.BooleanField(default = False, verbose_name='Staff')
    objects = UserManager()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, verbose_name='Rol', null=True, blank=True, default=None)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

