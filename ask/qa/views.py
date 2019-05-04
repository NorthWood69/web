# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from .models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from .forms import AskForm, AnswerForm, LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

@require_GET
def index(request, *args, **kwargs):
    questions = Question.objects.order_by('-id')
    paginator, page, limit = paginate(request, questions)
    context = {
        'title': 'Список вопросов',
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
        'title': 'Популярные вопросы',
        'questions': page,
        'paginator': paginator,
        'limit': limit,
    }
    return render(request, 'popular.html', context)

def question(request, question_id):
    q = get_object_or_404(Question, id=question_id)
    #a = q.answer_set.all()
    a = Answer.objects.filter(question=question_id).order_by('-added_at')
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            msg = 'Благодарим Вас за ответ!'
            form._user = request.user
            _ = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial = {'question': q.id})
    context = {
        'title': 'Страница вопроса',
        'question': q,
        'answers': a,
        'form': form,
    }
    return render(request, 'question.html', context)

def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    context = {
        'title': 'Задать вопрос',
        'form': form,
    }
    return render(request, 'ask.html', context)

def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    context = {
        'title': 'Вход на сайт',
        'form': form,
    }
    return render(request, 'login.html', context)

def log_out(request):
    if request.user is not None:
        logout(request)
        return HttpResponseRedirect(reverse('index'))

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.raw_passwrd
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SignupForm()
    context = {
        'title': 'Регистрация пользователя',
        'form': form,
    }
    return render(request, 'signup.html', context)

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
