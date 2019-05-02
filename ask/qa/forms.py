# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Question, Answer
from datetime import datetime
from django.contrib.auth import authenticate, login

class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip() == '':
            raise forms.ValidationError('The title field can not be empty', code='validation_error')
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('The text field can not be empty', code='validation_error')
        return text

    def save(self):
        if self._user.is_anonymous():
            self.cleaned_data['author_id'] = 1
        else:
            self.cleaned_data['author'] = self._user
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '': 
            raise forms.ValidationError('The text field can not be empty', code='validation_error')
        return text

    def clean_question(self):
        try:
            question = int(self.cleaned_data['question'])
        except ValueError:
            raise forms.ValidationError('Invalid data', code='validation_error')
        return question

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(
            Question,
            pk=self.cleaned_data['question'])
        if self._user.is_anonymous():
            self.cleaned_data['author_id'] = 1
        else:
            self.cleaned_data['author'] = self._user
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('The username field can not be empty', code='validation_error')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('The username used by another user')
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('The email field can not be empty', code='validation_error')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('The password field can not be empty', code='validation_error')
        self.raw_passeord = password
        return password

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        #auth = authenticate(**self.cleaned_data)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('The username field can not be empty', code='validation_error')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('The password field can not be empty', code='validation_error')
        return password

#    def save(self):
#        auth = authenticate(**self.cleaned_data)
#        return auth

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Wrong password or username')
        if not user.check_password(password):
            raise forms.ValidationError('Wrong password or username')
