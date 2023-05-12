from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .models import Folder
from .models import Permission

def folder_create(request) :
    if request.method == 'POST' :
            data = JSONParser().parse(request)
            


def folder_deleter(request) :


def folder_update(request) :


def folder_move(request) :
