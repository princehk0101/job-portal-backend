from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['owner']

    def validate(self, data):
        user = self.context['request'].user

        if Company.objects.filter(owner=user).exists():
            raise serializers.ValidationError("You already created a company.")

        return data