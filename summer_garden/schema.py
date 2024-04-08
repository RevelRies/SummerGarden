import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import ObjectType as GraphQLObjectType
from django.contrib.postgres.search import TrigramSimilarity

from .models import Object, ObjectImage, ObjectType, Quiz, Question, Answer


# GraphQL типы для моделей
class ObjectGraphQLType(DjangoObjectType):
    class Meta:
        model = Object
        fields = ("id", "name", "author", "info", "longitude", "latitude", "type", 'images')


class ObjectImageGraphQLType(DjangoObjectType):
    class Meta:
        model = ObjectImage


class ObjectTypeGraphQLType(DjangoObjectType):
    class Meta:
        model = ObjectType


class QuizGraphQLType(DjangoObjectType):
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions']


class QuestionGraphQLType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ['id', 'text', 'image_base64', 'answers']


class AnswerGraphQLType(DjangoObjectType):
    class Meta:
        model = Answer


# GraphQL запросы
class Query(GraphQLObjectType):
    # запросы и данные которые нужно в них передать
    object = graphene.Field(ObjectGraphQLType, id=graphene.Int())
    objects = graphene.List(ObjectGraphQLType)
    objects_by_type = graphene.List(ObjectGraphQLType, type_id=graphene.Int())
    objects_by_name = graphene.List(ObjectGraphQLType, object_name=graphene.String())
    object_types = graphene.List(ObjectTypeGraphQLType)
    quiz = graphene.Field(QuizGraphQLType, quiz_id=graphene.Int())
    quizzes = graphene.List(QuizGraphQLType)
    question = graphene.Field(QuestionGraphQLType, question_id=graphene.Int())

    # функции которые будут отрабатывать при обращении к запросам (выше)
    def resolve_object(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return Object.objects.get(id=id)
        return None

    def resolve_objects(self, info, **kwargs):
        return Object.objects.all()

    def resolve_objects_by_type(self, info, **kwargs):
        type_id = kwargs.get('type_id')

        if type_id:
            return Object.objects.filter(type=type_id)
        return None

    def resolve_objects_by_name(self, info, **kwargs):
        object_name = kwargs.get('object_name')

        if object_name:
            return (Object.objects.annotate(similarity=TrigramSimilarity('name', object_name),)
                    .filter(similarity__gt=0.1).order_by('-similarity'))
        return None

    def resolve_object_types(self, info, **kwargs):
        return ObjectType.objects.all()

    def resolve_quiz(self, info, **kwargs):
        quiz_id = kwargs.get('quiz_id')

        if quiz_id:
            return Quiz.objects.get(id=quiz_id)
        return None

    def resolve_quizzes(self, info, **kwargs):
        return Quiz.objects.all()

    def resolve_question(self, info, **kwargs):
        question_id = kwargs.get('question_id')

        if question_id:
            return Question.objects.get(id=question_id)
        return None


schema = graphene.Schema(query=Query)
