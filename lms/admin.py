from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'description')
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'description', 'link_to_video', 'course')
    list_filter = ('title', 'course',)
    search_fields = ('title', 'course',)
