from django.shortcuts import render

def index(request):
    """Home Page Of Learning Log"""
    return render(request,"learning_logs/index.html")
