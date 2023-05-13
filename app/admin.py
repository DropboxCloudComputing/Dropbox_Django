from django.contrib import admin
from .models import Files
from trash_bin.models import TrashBin

# Register your models here.
admin.site.register(Files)
admin.site.register(TrashBin)