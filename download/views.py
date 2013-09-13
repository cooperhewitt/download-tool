from django.shortcuts import render, redirect
from download.models import Download
import os
import cooperhewitt.api.client
import json

access_token = os.environ['CH_API_KEY']
hostname = os.environ['CH_API_HOST']

def index(request):
	context = {}
	return render(request, 'download/index.html', context)

def search(request):	
	try:
		query = request.POST['query']
	except (KeyError, Download.DoesNotExist):
		return redirect('/')
	else:
		results = search_objects(query)
		objects = results['objects']
		context = {'objects':objects}
		return render(request, 'download/search.html', context)
	
def thanks(request):
	context = {}
	return render(request, 'download/thanks.html', context)	

def search_objects(query):
	api = cooperhewitt.api.client.OAuth2(access_token, hostname=hostname)
	method = 'cooperhewitt.search.objects'
	args = { 'query': query, 'has_images': 'yes' }

	rsp = api.call(method, **args)
	
	return rsp
	