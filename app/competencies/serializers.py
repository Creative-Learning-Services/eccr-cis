from rest_framework import fields, serializers

from competencies.models import DjangoDomain


class DjangoDomainSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source='neo4j.uuid', read_only=True)
    name = serializers.CharField(source='neo4j.name', read_only=True)

    class Meta:
        model = DjangoDomain
        fields = ['uuid', 'name',]


class SpoofedSerializer(serializers.Serializer):
    """
    don't bother actually serializing, just convert to JSON
    """

    def to_representation(self, instance):
        return dict(instance.items())


class DynamicNodeSerializer(serializers.Serializer):
    """
    Dynamic serializer that creates field serializers upon instantiation
    """
    data_type_map = {
        'str': serializers.CharField,
        'uri': serializers.UUIDField,
        'datetime': serializers.DateTimeField,
        'bool': serializers.BooleanField,
        'int': serializers.IntegerField
    }
    data_type_key = 'data_type'
    multiple_expected_key = 'multiple_expected'

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        # get profile
        if profile is None and self.instance and hasattr(self.instance, 'profile') and\
                self.instance.profile:
            profile = self.instance.profile

        assert profile is not None, "No Profile provided or found on the instance"

        # TODO: resolve profile

        # for field in profile
        # self.fields[field_name] = serializer
        # ex
        # {'uuid': UUIDField(read_only=True, source='neo4j.uuid'),
        #  'name': CharField(read_only=True, source='neo4j.name')}
        # iterate fields in profile
        for field in profile:
            field_dict = profile[field]
            # get serializer ref based on data type
            field_serializer = self.type_serializer_map(
                field_dict[self.data_type_key])

            # if no serializer mapped skip this field
            if field_serializer is None:
                continue

            # if multiple expected
            if self.multiple_expected_key in field_dict and \
                    field_dict[self.multiple_expected_key]:
                # use list and get args for serializer
                self.fields[field] = serializers.ListField(child=field_serializer(
                    **self.serializer_args(field, field_dict, field_serializer)))
            else:
                # get serializer args
                self.fields[field] = field_serializer(
                    **self.serializer_args(field, field_dict, field_serializer))

    def type_serializer_map(self, data_type: str) -> fields.Field | None:
        """
        Given a string of type from schema
        return serializer field REFERENCE
        """
        if data_type.lower() in self.data_type_map:
            return self.data_type_map[data_type.lower()]
        return None

    def serializer_args(self, field: str, schema: dict, serializer: fields.Field) -> dict:
        """
        Params:
            field (str): field name
            schema (dict): dict containing schema info of this field
            serializer (fields.Field): serializer to be used
        Returns:
            dict of any arguments to pass into the serializer
        """
        ret_dict = {}
        if isinstance(serializer, serializers.UUIDField):
            ret_dict['format'] = 'hex'

        return ret_dict

    def create(self, validated_data):
        """
        Make Neo4j query to create obj
        """
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Make Neo4j query to update existing obj
        """
        return super().update(instance, validated_data)
