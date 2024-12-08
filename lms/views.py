from rest_framework import viewsets, generics
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.permissions import IsOwnerOrStaff
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from lms.tasks import course_update


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsModerator | IsOwner]
        else:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        course_update.delay(instance.pk)
        return instance


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [~IsModerator, IsOwner]
        else:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator | IsOwner, IsAuthenticated)


class SubscriptionCreateApiView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course)
        subs_item = Subscription.objects.filter(course=course, user=user)

        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)  # Создаем подписку
            message = 'подписка добавлена'
        return Response({"message": message})
