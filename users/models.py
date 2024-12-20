from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=50, **NULLABLE, verbose_name="Город", help_text="Укажите ваш город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="payments", **NULLABLE
    )
    payment_date = models.DateField(verbose_name="Дата платежа", **NULLABLE)
    payment_lesson = models.ForeignKey(
        "lms.Lesson", on_delete=models.CASCADE, **NULLABLE, related_name="payments"
    )
    payment_course = models.ForeignKey(
        "lms.Course", on_delete=models.CASCADE, **NULLABLE, related_name="payments"
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты", default=0)
    CASH = "cash"
    NON_CASH = "non_cash"
    PAYMENT_METHOD = [(CASH, "cash"), (NON_CASH, "non_cash")]
    payment_method = models.CharField(
        choices=PAYMENT_METHOD, default=CASH, verbose_name="Способ оплаты"
    )
    session_id = models.CharField(max_length=255, verbose_name='Id сессии', help_text='Укажите id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', help_text='Укажите ссылку на оплату',
                           **NULLABLE)

    def __str__(self):
        return f"{self.amount} - {self.payment_method}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)


