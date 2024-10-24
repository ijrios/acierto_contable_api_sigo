from django.db import models
from accounting_success.base_model import BaseModel
from django.contrib.sessions.models import Session

class TokenSiigo(BaseModel):
    token = models.TextField()
    created = models.DateField(auto_now=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default=None, null=True, blank=True)
    
    class  Meta:
        db_table = 'token_siigo'
