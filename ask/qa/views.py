# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from .models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
#from .forms import AskForm, AnswerForm, LoginForm, SignupForm
#from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

@require_GET
def index(request, *args, **kwargs):
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
    #return render(request, 'qa/index.html', context)
    return HttpResponse('OK')

def question(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    a = q.answer_set.all()
    #a = Answer.objects.filter(question=question_id).order_by('-added_at')
    form = AnswerForm(initial = {'question': question_id})
    context = {'question': q, 'answers': a, 'form': form, }
    return render(request, 'question.html', context)
