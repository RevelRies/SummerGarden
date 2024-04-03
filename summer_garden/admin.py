import nested_admin


from django.db import models
from django.forms import Textarea
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Object, ObjectType, ObjectImage, Quiz, Question, Answer


admin.site.unregister(Group)
admin.site.unregister(User)


# Объект
class ObjectImagesInline(admin.StackedInline):
    model = ObjectImage
    extra = 1
    exclude = ['image_base64']


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [ObjectImagesInline]


# Тип объекта
@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    pass


# Викторина
class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 60})},
    }


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    exclude = ['image_base64']
    inlines = [AnswerInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 90})},
    }


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]