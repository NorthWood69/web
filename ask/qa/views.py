# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from .models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from .forms import AskForm, AnswerForm
#from .forms import AskForm, AnswerForm, LoginForm, SignupForm
#from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

@require_GET
def idx(request, *args, **kwargs):
    question_list = Question.objects.order_by('-id')
    paginator, page, limit = paginate(request, question_list)
    context = {
        'questions': page,
        'paginator': paginator,
        'limit': limit,
    }
    return render(request, 'index.html', context)

@require_GET
def popular(request, *args, **kwargs):
    question_list = Question.objects.order_by('-rating')
    paginator, page, limit = paginate(request, question_list)    
    context = {
        'questions': page,
        'paginator': paginator,
        'limit': limit,
    }
    return render(request, 'popular.html', context)

def test(request, *args, **kwargs):
    context = {'var1': 1, 'var2': 2}
    #return render(request, 'index.html', context)
    return HttpResponse('OK')

#def question(request, question_id):
#    q = get_object_or_404(Question, id=question_id)
#    #a = q.answer_set.all()
#    a = Answer.objects.filter(question=question_id).order_by('-added_at')
#    form = AnswerForm(initial = {'question': question_id})
#    context = {'question': q, 'answers': a, 'form': form, }
#    return render(request, 'question.html', context)

def question(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            _ = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': q.id})
    return render(request, 'question.html', {'question': q,
                                             'form': form, })

def ask(request, *args, **kwargs):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {'form': form})

#def answer(request):
#    if request.method == 'POST':
#        form = AnswerForm(request.POST)
#        if form.is_valid():
#            print('Answer is valid')
#            form._user = request.user
#            answer = form.save()
#            url = answer.get_url()
#        return HttpResponseRedirect(url)
#    return HttpResponseRedirect('/')

def paginate(request, lst):
    # get limit
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    # if limit is too high, normalize it
    if limit > 100:
        limit = 10
    paginator = Paginator(lst, limit)
    # get current page
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page, limit
