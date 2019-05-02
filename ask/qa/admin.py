# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from qa.models import Question, Answer

admin.site.register(Question)
admin.site.register(Answer)