import graphene

from django_filters import FilterSet, OrderingFilter

from graphene import Node
from graphene.utils.str_converters import to_snake_case
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import ObjectType as GraphQLObjectType
from django.contrib.postgres.search import TrigramSimilarity

from .models import Object, ObjectImage, ObjectType, Quiz, Question, Answer


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    '''
    Переопределение класса для того чтобы order_by работал вместе с фильтрами
    https://zainp.com/add-ordering-django-graphql/
    '''
    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args, filtering_args, filterset_class
    ):
        qs = super().resolve_queryset(
            connection, iterable, info, args, filtering_args, filterset_class
        )
        order = args.get("orderBy", None)
        if order:
            if isinstance(order, str):
                snake_order = to_snake_case(order)
            else:
                snake_order = [to_snake_case(o) for o in order]

            # annotate counts for ordering
            for order_arg in snake_order:
                order_arg = order_arg.lstrip("-")
                annotation_name = f"annotate_{order_arg}"
                annotation_method = getattr(qs, annotation_name, None)
                if annotation_method:
                    qs = annotation_method()

            # override the default distinct parameters
            # as they might differ from the order_by params
            qs = qs.order_by(*snake_order).distinct()

        return qs


# GraphQL типы для моделей
class ObjectGraphQLType(DjangoObjectType):
    # для того чтобы в ответе отображалось id django модели, а не id Node
    pk = graphene.Int(source='pk')

    class Meta:
        model = Object
        fields = "__all__"
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'author': ['exact', 'icontains', 'istartswith'],
            'type__name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (Node,)


class ObjectImageGraphQLType(DjangoObjectType):
    class Meta:
        model = ObjectImage


class ObjectTypeGraphQLType(DjangoObjectType):
    # для того чтобы в ответе отображалось id django модели, а не id Node
    pk = graphene.Int(source='pk')

    class Meta:
        model = ObjectType
        fields = "__all__"
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (Node,)


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
    object = graphene.Field(ObjectGraphQLType, pk=graphene.Int())
    objects = OrderedDjangoFilterConnectionField(ObjectGraphQLType, orderBy=graphene.List(of_type=graphene.String))
    object_types = OrderedDjangoFilterConnectionField(ObjectTypeGraphQLType, orderBy=graphene.List(of_type=graphene.String))
    quiz = graphene.Field(QuizGraphQLType, quiz_pk=graphene.Int())
    quizzes = graphene.List(QuizGraphQLType)
    question = graphene.Field(QuestionGraphQLType, question_id=graphene.Int())

    # функции которые будут отрабатывать при обращении к запросам (выше)
    def resolve_object(self, info, **kwargs):
        id = kwargs.get('pk')

        if id:
            return Object.objects.get(id=id)
        return None

    def resolve_objects(self, info, **kwargs):
        return Object.objects.all()

    def resolve_object_types(self, info, **kwargs):
        return ObjectType.objects.all()

    def resolve_quiz(self, info, **kwargs):
        quiz_id = kwargs.get('quiz_pk')

        if quiz_id:
            return Quiz.objects.get(id=quiz_id)
        return None

    def resolve_quizzes(self, info, **kwargs):
        return Quiz.objects.all()

    def resolve_question(self, info, **kwargs):
        question_id = kwargs.get('question_pk')

        if question_id:
            return Question.objects.get(id=question_id)
        return None


schema = graphene.Schema(query=Query)
