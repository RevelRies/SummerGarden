import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.types import ObjectType as GraphQLObjectType
from django.contrib.postgres.search import TrigramSimilarity

from .models import Object, ObjectImage, ObjectType, Quiz, Question, Answer


# GraphQL типы для моделей
class ObjectGraphQLType(DjangoObjectType):
    class Meta:
        model = Object


class ObjectImageGraphQLType(DjangoObjectType):
    class Meta:
        model = ObjectImage


class ObjectTypeGraphQLType(DjangoObjectType):
    class Meta:
        model = ObjectType


class QuizGraphQLType(DjangoObjectType):
    class Meta:
        model = Quiz


class QuestionGraphQLType(DjangoObjectType):
    class Meta:
        model = Question


class AnswerGraphQLType(DjangoObjectType):
    class Meta:
        model = Answer


# GraphQL запросы
class Query(GraphQLObjectType):
    object = graphene.Field(ObjectGraphQLType, id=graphene.Int())
    objects = graphene.List(ObjectGraphQLType)
    object_images = graphene.List(ObjectImageGraphQLType, object_id=graphene.Int())
    objects_by_type = graphene.List(ObjectGraphQLType, type_id=graphene.Int())
    objects_by_name = graphene.List(ObjectGraphQLType, object_name=graphene.String())
    object_types = graphene.List(ObjectTypeGraphQLType)
    quizzes = graphene.List(QuizGraphQLType)
    questions_by_quiz = graphene.List(QuestionGraphQLType, quize_id=graphene.Int())
    answer_by_question = graphene.List(AnswerGraphQLType, question_id=graphene.Int())

    def resolve_object(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return Object.objects.get(id=id)
        return None

    def resolve_objects(self, info, **kwargs):
        return Object.objects.all()

    def resolve_object_images(self, info, **kwargs):
        object_id = kwargs.get('object_id')

        if object_id:
            return ObjectImage.objects.filter(object=object_id)
        return None

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

    def resolve_quizzes(self, info, **kwargs):
        return Quiz.objects.all()

    def resolve_questions_by_quiz(self, info, **kwargs):
        quize_id = kwargs.get('quize_id')

        if quize_id:
            return Question.objects.filter(quiz=quize_id)
        return None

    def resolve_answer_by_question(self, info, **kwargs):
        question_id = kwargs.get('question_id')

        if question_id:
            return Answer.objects.filter(question=question_id)
        return None

schema = graphene.Schema(query=Query)
