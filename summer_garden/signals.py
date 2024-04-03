import base64

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import ObjectImage, Question


@receiver(post_save, sender=ObjectImage)
def get_base64_from_objects_image(sender, instance, **kwargs):
    with open(instance.image.path, "rb") as image:
        base64_text = str(base64.b64encode(image.read()))[2:-1]

    # Обновляю данные модели
    ObjectImage.objects.filter(id=instance.id).update(image_base64=base64_text)


@receiver(post_save, sender=Question)
def get_base64_from_question_image(sender, instance, **kwargs):
    print('сохранение вопроса')
    print(instance.image.path)
    with open(instance.image.path, "rb") as image:
        base64_text = str(base64.b64encode(image.read()))[2:-1]

    # Обновляю данные модели
    Question.objects.filter(id=instance.id).update(image_base64=base64_text)