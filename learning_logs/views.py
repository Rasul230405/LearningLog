from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Home Page Of Learning Log"""
    return render(request,"learning_logs/index.html")

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {'topics':topics}
    return render(request,"learning_logs/topics.html",context)
    if topic.owner != request.user:
        raise Http404

@login_required
def topic(request, topic_id):
    """Entry page""" 
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request,"learning_logs/topic.html",context)   

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}    
    return render(request,"learning_logs/new_topic.html",context)

@login_required
def new_entry(request, topic_id):
    """User add entry assosited with topic"""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            my_entry = form.save(commit=False)
            my_entry.topic = topic
            my_entry.save()
            return HttpResponseRedirect(reverse('topic',args=[topic_id]))

    context = {'topic': topic,'form': form}
    return render(request,"learning_logs/new_entry.html",context)

@login_required
def edit_entry(request, entry_id):
    """Edit existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect(reverse('topic',args=[topic.id]))

    context = {'topic': topic, 'entry': entry, 'form': form}
    return render(request,"learning_logs/edit_entry.html",context)                       