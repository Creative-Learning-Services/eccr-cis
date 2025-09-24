from rest_framework import serializers

from eccr.serializers.competency import (
    CompetencySerializer,
)


class RequiresRelSerializer(serializers.Serializer):
    rationale = serializers.CharField(required=False, allow_blank=True)
    criticality = serializers.CharField(required=False, allow_blank=True)


class DependsOnRelSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True)


class IsPartOfRelSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True)


class IncludesCompetencyRelSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True)


class HasCompetencyRelSerializer(serializers.Serializer):
    competency_order = serializers.IntegerField(required=False)
    proficiency_level = serializers.CharField(required=False, allow_blank=True)
    assessment_method = serializers.CharField(required=False, allow_blank=True)
    training_hours = serializers.IntegerField(required=False)
    certification_required = serializers.BooleanField(required=False)
    last_updated = serializers.DateTimeField(required=False)
    version = serializers.CharField(required=False, allow_blank=True)


# Combined serializers for entities with their relationships
class CompetencyWithRelationshipSerializer(serializers.Serializer):
    competency = CompetencySerializer()
    relationship_properties = HasCompetencyRelSerializer()


# class WorkRoleWithKSATSSerializer(serializers.Serializer):
#     work_role = WorkRoleSerializer()
#     ksats = serializers.ListField(child=serializers.DictField())
