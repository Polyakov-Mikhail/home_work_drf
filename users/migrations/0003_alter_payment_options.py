# Generated by Django 5.1.3 on 2024-11-27 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payment",
            options={
                "ordering": ("-payment_date",),
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
