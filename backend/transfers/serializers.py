from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

from transfers.models import Transfer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'get_full_name')


class TransferSerializer(serializers.Serializer):
    from_user_id = serializers.IntegerField()
    to_inn = serializers.CharField(max_length=12, validators=[
        int_list_validator(sep='', message=None, code='invalid', allow_negative=False)])
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)

    def create(self, validated_data):
        return Transfer(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
