# Generated by Django 4.2.2 on 2023-07-04 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_type',
        ),
        migrations.AddField(
            model_name='customuser',
            name='account_status',
            field=models.CharField(choices=[('verfied', 'Verified'), ('not_verified', 'Not Verified')], default='not_verified', max_length=20),
        ),
    ]
