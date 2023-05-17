from django.db import models
from user_app.models import Users
from django.conf import settings


# Create your models here.
class Folder(models.Model):
    id = models.BigIntegerField(primary_key=True)
    folder_name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    users = models.ForeignKey(Users, models.DO_NOTHING)
    pfolder = models.ForeignKey('self', models.DO_NOTHING, db_column="folder_id")
    removed = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'folder'

    def __iter__(self):
        yield {
            "id": self.id,
            "folder_name": self.folder_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "users": self.users,
            "pfolder":self.pfolder
        }


class Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
    users = models.ForeignKey(Users, models.DO_NOTHING)
    folder = models.ForeignKey(Folder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'permission'
