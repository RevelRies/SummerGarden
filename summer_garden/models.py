from django.db import models


class ObjectType(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип объекта'
        verbose_name_plural = 'Типы объектов'

    def __str__(self):
        return f"{self.name}"


class Object(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    author = models.CharField(max_length=250, verbose_name='Автор')
    info = models.TextField(max_length=1000, verbose_name='Описание')
    latitude = models.CharField(max_length=100, verbose_name='Широта')
    latitude_conv = models.CharField(max_length=100, verbose_name='Конвертированная широта', blank=True)
    longitude = models.CharField(max_length=100, verbose_name='Долгота')
    longitude_conv = models.CharField(max_length=100, verbose_name='Конвертированная долгота', blank=True)
    type = models.ForeignKey(to=ObjectType, on_delete=models.CASCADE, verbose_name='Тип')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return f"{self.name}"


class ObjectImage(models.Model):
    image = models.ImageField(upload_to='objects_images', verbose_name='Изображение объекта')
    image_base64 = models.TextField(blank=True, verbose_name='base64 кодировка фотографии')
    object = models.ForeignKey(to=Object, on_delete=models.CASCADE, verbose_name='Объект', related_name='images')

    class Meta:
        verbose_name = 'Изображение объекта'
        verbose_name_plural = 'Изображения объектов'

    def __str__(self):
        return f"{self.object.name} - изображение"


class Quiz(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    text = models.TextField(max_length=100, verbose_name='Текст вопроса')
    image = models.ImageField(upload_to='questions_images', verbose_name='Изображение вопроса')
    image_base64 = models.TextField(blank=True, verbose_name='base64 кодировка фотографии')
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, verbose_name='Викторина', related_name='questions')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f"{self.text[:20]}"


class Answer(models.Model):
    text = models.TextField(max_length=300, verbose_name='Текст ответа')
    right = models.BooleanField(verbose_name='Правильный ответ')
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f"{self.text[:20]}"