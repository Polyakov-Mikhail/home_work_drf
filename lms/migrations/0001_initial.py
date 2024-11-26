# Generated by Django 5.1.3 on 2024-11-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Укажите название курса",
                        max_length=100,
                        verbose_name="Название",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите превью курса (картинка)",
                        null=True,
                        upload_to="lms/course/preview/",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Укажите описание курса", verbose_name="Описание"
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Укажите название урока",
                        max_length=100,
                        verbose_name="Название",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Укажите описание урока", verbose_name="Описание"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите превью урока (картинка)",
                        null=True,
                        upload_to="lms/lesson/preview/",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "link_to_video",
                    models.URLField(
                        help_text="Укажите ссылку на видео",
                        verbose_name="Ссылка на видео",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
