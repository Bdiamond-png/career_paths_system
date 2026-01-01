from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. Suck me!")


def new(request):
    return HttpResponse("Fuck a nigga named Mosh")