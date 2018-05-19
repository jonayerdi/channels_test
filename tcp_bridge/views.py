from django.shortcuts import render
from django.http import HttpResponse
from .models import Text
import json

#Web Pages
def index(request):
	return render(request, 'index.html')

#REST API
def api(request):
	text = Text.objects.last()
	content = json.dumps({'text': text.text}, indent=4)
	return HttpResponse(content=content, content_type='application/json')
