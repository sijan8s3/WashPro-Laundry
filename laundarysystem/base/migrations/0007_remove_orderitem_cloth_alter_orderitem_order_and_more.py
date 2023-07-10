# Generated by Django 4.2.2 on 2023-07-09 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='cloth',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='base.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='cloth',
            field=models.ManyToManyField(related_name='cloth', to='base.clothes'),
        ),
    ]