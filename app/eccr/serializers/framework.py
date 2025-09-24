from rest_framework import serializers


class FrameworkSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    authoritative_source = serializers.CharField(required=False, allow_blank=True)
    # Stored as a list in test data creation
    resource_association = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    association = serializers.CharField(required=False, allow_blank=True)
    PROFILE = serializers.ListField(child=serializers.CharField(), required=False)
    competency_count = serializers.IntegerField(required=False)
    domain = serializers.CharField(required=False, allow_blank=True)
    conformsTo = serializers.CharField(required=False, allow_blank=True)


class FrameworkWithCompetenciesSerializer(serializers.Serializer):
    framework = FrameworkSerializer()
    competencies = serializers.ListField(child=serializers.DictField())
