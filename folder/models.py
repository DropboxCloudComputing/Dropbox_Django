from django.db import models

# Create your models here.
class Folder(models.Model):
    id = models.BigIntegerField(primary_key=True)
    folder_name = models.CharField(max_length=45)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    folder = models.ForeignKey('self', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'folder'


class Permission(models.Model):
    id = models.BigIntegerField(primary_key=True)
    users = models.ForeignKey('Users', models.DO_NOTHING)
    folder = models.ForeignKey(Folder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'permission'