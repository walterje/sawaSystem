from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from SAWA_SYS.settings import MEDIA_URL, STATIC_URL
from crum import get_current_request


class User(AbstractUser):
    imagen = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/admin.JPG')
    
    def get_nombre_usuario_completo (self):
        return '{} {} '.format(self.first_name, self.last_name)
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['imagen'] = self.get_imagen()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        item['nombre_usuario_completo'] = self.get_nombre_usuario_completo()
        return item
    
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
    
    