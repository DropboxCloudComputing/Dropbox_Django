# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Files(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    size = models.IntegerField()
    folder = models.ForeignKey('Folder', models.DO_NOTHING)
    memo = models.CharField(max_length=255, blank=True, null=True)
    version = models.IntegerField()
    last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'files'


class Folder(models.Model):
    title = models.CharField(max_length=255)
    folder_id = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'folder'


class Permission(models.Model):
    folder = models.OneToOneField(Folder, models.DO_NOTHING, primary_key=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'


class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    password_change_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
