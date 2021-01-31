import graphene

from graphene_django import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField


class CityNode(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = ['city_name']
        interfaces = (graphene.relay.Node,)


class TitleNode(DjangoObjectType):
    class Meta:
        model = Title
        filter_fields = ['title_name']
        interfaces = (graphene.relay.Node,)


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = [
            'employee_name',
            'employee_city__city_name',
            'employee_title__title_name'
        ]
        interfaces = (graphene.relay.Node,)


class CreateTitle(graphene.Mutation):
    title = graphene.Field(lambda: TitleNode)

    class Arguments:
        title_name = graphene.String()

    def mutate(self, info, title_name):
        title = Title(title_name=title_name)
        title.save()
        return CreateTitle(title=title)


class UpdateTitle(graphene.Mutation):
    title = graphene.Field(lambda: TitleNode)

    class Arguments:
        id = graphene.String()
        title_name = graphene.String()

    def mutate(self, info, id, title_name):
        title = Title.objects.get(pk=id)
        title.title_name = title_name
        title.save()
        return UpdateTitle(title=title)


class DeleteTitle(graphene.Mutation):
    title = graphene.Field(TitleNode)

    class Input:
        id = graphene.String()

    def mutate(root, info, id):
        title = Title.objects.get(pk=id)
        title.delete()
        return DeleteTitle(title=title)


class Query(object):
    city = graphene.relay.Node.Field(CityNode)
    all_cities = DjangoFilterConnectionField(CityNode)

    title = graphene.relay.Node.Field(TitleNode)
    all_titles = DjangoFilterConnectionField(TitleNode)

    employee = graphene.relay.Node.Field(EmployeeNode)
    employees = DjangoFilterConnectionField(EmployeeNode)


class Mutation(graphene.ObjectType):
    create_title = CreateTitle.Field()
    update_title = UpdateTitle.Field()
    delete_title = DeleteTitle.Field()
