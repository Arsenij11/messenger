# Generated by Django 5.1.4 on 2024-12-24 16:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_alter_chat_is_private'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL, verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='admin',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatadmin', to='API.account'),
        ),
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.account')),
            ],
        ),
        migrations.AlterField(
            model_name='chat',
            name='is_private',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chatseconduser', to='API.privatechat', verbose_name='Приватный чат'),
        ),
    ]