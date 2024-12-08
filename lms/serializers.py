from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from lms.validators import validate_youtube_only

from lms.models import Course, Lesson, Subscription


class LessonSerializer(ModelSerializer):
    link_to_video = serializers.URLField(validators=[validate_youtube_only])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, course):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=course).exists()

    class Meta:
        model = Course
        fields = ("id", "title", "description", "lessons_count", "lessons")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("sign_of_subscription",)
