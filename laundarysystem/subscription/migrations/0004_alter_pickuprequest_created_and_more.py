# Generated by Django 4.2.2 on 2023-07-14 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_pickuprequest_created_pickuprequest_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickuprequest',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pickuprequest',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]