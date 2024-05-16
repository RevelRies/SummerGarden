import base64

from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Object, ObjectImage, Question


# переводит изображение в base64 при сохранении объекта
@receiver(post_save, sender=ObjectImage)
def get_base64_from_objects_image(sender, instance, **kwargs):
    print('сохранено изображение')
    with open(instance.image.path, "rb") as image:
        base64_text = str(base64.b64encode(image.read()))[2:-1]

    # Обновляю данные модели
    ObjectImage.objects.filter(id=instance.id).update(image_base64=base64_text)


# переводит изображение в base64 при сохранении вопроса
@receiver(post_save, sender=Question)
def get_base64_from_question_image(sender, instance, **kwargs):
    with open(instance.image.path, "rb") as image:
        base64_text = str(base64.b64encode(image.read()))[2:-1]

    # Обновляю данные модели
    Question.objects.filter(id=instance.id).update(image_base64=base64_text)


# если при сохранении объекта к нему не было добавлено ни одного изображения,
# то автоматически добавляется дефолтное
# @receiver(post_save, sender=Object)
# def check_object_image(sender, instance, **kwargs):
#     if not instance.images.exists():












