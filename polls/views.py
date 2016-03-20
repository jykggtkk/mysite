from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#http://python.usyiyi.cn/django/intro/tutorial03.html
def index(request):
	return HttpResponse("Hello,world.You're at the polls index.")
def results(request,question_id):
    response="You're looking at the results of quesiton %s"  
    return HttpResponse(response % question_id)
def detail(request,question_id):
    return HttpResponse("You're looking at the results of quesiton %s" % question_id)
def vote(request,question_id):
    return HttpResponse("You're voting on quesiton %s" % question_id)