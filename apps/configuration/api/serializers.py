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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation["payment_info"] is not None:
            representation["payment_info"] = representation["payment_info"].replace("\n", "<br>")
        if representation["content"] is not None:
            representation["content"] = representation["content"].replace("\n", "<br>")

        return representation

