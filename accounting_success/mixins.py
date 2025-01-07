from rest_framework.exceptions import PermissionDenied

class UserRoleMixin:
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def get_user_role_permissions(self, user):
        
        if not user.is_authenticated:
            raise PermissionDenied("Usuario no autenticado.")
            
        role = user.role
        if not role:
            raise PermissionDenied("El usuario no tiene el rol asignado.")
        
        role_permissions = role.permissions
        
        if isinstance(role_permissions, str):
            import json
            role_permissions = json.loads(role_permissions)
        
        return role_permissions

    def check_permissions(self, required_permission):
        user = self.request.user
        
        if user.is_staff:
            return True
        
        user_permissions = self.get_user_role_permissions(user)
        
        if required_permission not in user_permissions:
            raise PermissionDenied("El usuario no tiene los permisos necesarios.")
        
        return True