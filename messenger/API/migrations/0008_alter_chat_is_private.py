# Generated by Django 5.1.4 on 2024-12-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_chat_chat_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='is_private',
            field=models.BooleanField(null=True),
        ),
    ]