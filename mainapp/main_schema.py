import graphene
import summer_garden.schema


class Query(summer_garden.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)