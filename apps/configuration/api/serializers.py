from rest_framework import serializers

from apps.configuration.models import PersonalInfo


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = (
            "method",
            "payment_info",
            "content",
        )
