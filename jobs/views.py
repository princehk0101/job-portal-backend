from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Job
from .serializers import JobSerializer
from .permissions import IsEmployer


# ==========================================
# Job List (Search + Filter + Ordering)
# ==========================================
class JobListView(ListAPIView):
    queryset = Job.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 🔥 Improved filtering
    filterset_fields = {
        'location': ['exact', 'icontains'],
        'salary': ['gte', 'lte'],
        'experience_required': ['gte'],
        'job_type': ['exact'],
    }

    search_fields = ['title', 'description']
    ordering_fields = ['salary', 'created_at']


# ==========================================
# Create Job (Employer Only)
# ==========================================
class JobCreateView(CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


# ==========================================
# Job Detail
# ==========================================
class JobDetailView(RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [AllowAny]


# ==========================================
# Update Job (ONLY OWNER CAN UPDATE)
# ==========================================
class JobUpdateView(UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(
            employer=self.request.user,
            is_active=True
        )


# ==========================================
# Soft Delete Job (ONLY OWNER CAN DELETE)
# ==========================================
class JobDeleteView(DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(
            employer=self.request.user
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()