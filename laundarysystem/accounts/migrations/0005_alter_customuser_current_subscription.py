# Generated by Django 4.2.2 on 2023-07-08 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_order_status'),
        ('accounts', '0004_customuser_address_customuser_current_subscription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='current_subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.subscription'),
        ),
    ]
