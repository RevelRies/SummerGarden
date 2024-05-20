import nested_admin

from django.db import models
from django.forms import Textarea, BaseInlineFormSet
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe

from .models import Object, ObjectType, ObjectImage, Quiz, Question, Answer


admin.site.unregister(Group)
admin.site.unregister(User)


class RequiredFormSet(BaseInlineFormSet):
    '''
    Определение формы для того чтобы объект нельзя было сохранить, если не добавлено хотя бы 1 изображение
    Так же если удалить единственное изображение - объект не сохранится
    '''
    def is_valid(self):
        return super().is_valid() and not any([bool(e) for e in self.errors])

    def clean(self):
        # получаем формы изображений и считаем их количество
        count = 0
        for form in self.forms:
            try:
                # счетчик прибавляет +1 если форма существует и на ней не стоит флажок удалить
                # это сделано для того чтобы хотя бы на одной форме не стоял флажок удалить
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    count += 1
            except AttributeError:
                pass
        # если есть хотя бы одна форма, то объект сохраняется
        if count < 1:
            raise ValidationError('Обязательно должно быть хотя бы одно изображение')


# Объект
class ObjectImagesInline(admin.StackedInline):
    model = ObjectImage
    extra = 1
    exclude = ['image_base64']
    formset = RequiredFormSet
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [ObjectImagesInline]
    exclude = ['latitude_conv', 'longitude_conv']


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
    readonly_fields = ['preview']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 90})},
    }

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]