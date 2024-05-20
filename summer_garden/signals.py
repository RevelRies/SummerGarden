import base64

from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Object, ObjectImage, Question


# переводит изображение в base64 при сохранении изображения объекта
@receiver(post_save, sender=ObjectImage)
def get_base64_from_objects_image(sender, instance, **kwargs):
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


# конвертирует широту и долготу при сохранении объекта
@receiver(post_save, sender=Object)
def check_object_image(sender, instance, **kwargs):
    def conv_lat(lat: str) -> str:
        # конвертирование широты
        lat = float(lat)
        result = round(((lat - 30.3354) / 0.0062) * 800 + 400, 6)
        return str(result)
    def conv_lon(lon: str) -> str:
        # конвертирование долготы
        lon = float(lon)
        result = round(((lon - 59.94459) / 0.00628) * 1600 + 800, 6)
        return str(result)

    Object.objects.filter(id=instance.id).update(latitude_conv=conv_lat(instance.latitude),
                                              longitude_conv=conv_lon(instance.longitude))












