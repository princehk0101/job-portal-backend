from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    applicant_email = serializers.ReadOnlyField(source='applicant.email')
    job_title = serializers.ReadOnlyField(source='job.title')

    class Meta:
        model = Application
        fields = [
            'id',
            'applicant',
            'applicant_email',
            'job',
            'job_title',
            'full_name',
            'college_name',
            'phone_number',
            'resume',
            'cover_letter',
            'status',
            'applied_at',
        ]

        read_only_fields = [
            'applicant',
            'job',
            'status',
            'applied_at',
        ]

    def validate_resume(self, value):

        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError(
                "Only PDF files are allowed."
            )

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Resume file too large (Max 5MB)."
            )

        return value


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['status']