from uuid import UUID

from django.db import models
from django_neomodel import DjangoNode
from neomodel import (One, RelationshipTo, StringProperty, UniqueIdProperty,
                      ZeroOrOne)
from neomodel.contrib import SemiStructuredNode

# Create your models here.


class SemiStructuredDjangoNode(SemiStructuredNode, DjangoNode):
    __abstract_node__ = True


class DjangoSemiStructuredCompetency(SemiStructuredDjangoNode):
    uuid = UniqueIdProperty()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.inflate


# DOESN'T WORK for setting labels on write, could be used for pulling data out?
# class SCDNode(SemiStructuredDjangoNode):
#     uuid = UniqueIdProperty()

#     class Meta:
#         app_label = 'competencies'


class NeoDomain(SemiStructuredDjangoNode):
    uuid = UniqueIdProperty()
    name = StringProperty()
    # within = Relationship(SCDNode, 'WITHIN')

    class Meta:
        app_label = 'competencies'


class DjangoDomain(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, blank=False, null=False)

    def _get_neo4j_object(self) -> NeoDomain:
        if not isinstance(self.uuid, UUID):
            self.uuid = UUID(self.uuid)
        return NeoDomain.nodes.get(uuid=self.uuid.hex)

    neo4j = property(_get_neo4j_object)


class DirectoryStructure(DjangoNode):
    uuid = UniqueIdProperty()
    parent = RelationshipTo('DirectoryStructure', 'PARENT', ZeroOrOne)
    name = StringProperty(required=True)


class FileMixin():
    within = RelationshipTo('DirectoryStructure', 'WITHIN', One)


class Competency(SemiStructuredNode):
    uuid = UniqueIdProperty()


class CompetencyFramework(SemiStructuredNode):
    uuid = UniqueIdProperty()
    competencies = RelationshipTo(Competency, 'COMPETENCIES')


class CompetencyPermissions(models.Model):
    uuid = models.UUIDField(primary_key=True)

    def _get_neo4j_object(self) -> DjangoSemiStructuredCompetency:
        if not isinstance(self.uuid, UUID):
            self.uuid = UUID(self.uuid)
        return DjangoSemiStructuredCompetency.nodes.get(uuid=self.uuid.hex)

    neo4j = property(_get_neo4j_object)
