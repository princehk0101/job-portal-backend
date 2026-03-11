from rest_framework import serializers
from .models import Job, JobCategory



class JobCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = JobCategory
        fields = ["id", "name", "slug"]



class JobSerializer(serializers.ModelSerializer):

    employer_email = serializers.ReadOnlyField(source="employer.email")
    job_type_display = serializers.SerializerMethodField()

    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Job
        fields = [
            "id",
            "employer_email",
            "title",
            "description",
            "location",
            "salary",
            "job_type",
            "job_type_display",
            "experience_required",
            "category",        
            "category_name",   
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "employer_email",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_job_type_display(self, obj):
        return obj.get_job_type_display()