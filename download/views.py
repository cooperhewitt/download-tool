from django.shortcuts import render, redirect
from download.models import Download

def index(request):
	context = {}
	return render(request, 'download/index.html', context)

def search(request):
	context = {}
	return render(request, 'download/index.html', context)
	
