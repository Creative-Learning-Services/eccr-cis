import typing
from uuid import UUID

from django.db import models
from django.forms import ValidationError
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


class GenericNode():
    """
    Class to store generic attributes and relationships
    """

    def __init__(self, items: typing.ItemsView[str, typing.Any]):
        # self._attributes = set()
        for k, v in items:
            self._add_attr(k, v)

    def _add_attr(self, k, v):
        if hasattr(self, k):
            curr = getattr(self, k)
            if isinstance(curr, list):
                curr.append(v)
            else:
                setattr(self, k, [curr, v])
        else:
            setattr(self, k, v)
        # self._attributes.add(k)

    def __repr__(self):
        return str(vars(self))
        # {k: getattr(self, k) for k in self._attributes})


class Configuration(models.Model):
    """
    Model to store configuration values
    """
    ldss_host = models.CharField(
        help_text='Enter the host url for the LDSS (Schema Service) to use.',
        max_length=200
    )

    def save(self, *args, **kwargs):
        if not self.pk and Configuration.objects.exists():
            raise ValidationError('Configuration model already exists')
        return super(Configuration, self).save(*args, **kwargs)
