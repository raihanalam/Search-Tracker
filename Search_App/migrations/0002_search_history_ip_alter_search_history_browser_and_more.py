# Generated by Django 4.0.2 on 2022-02-11 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Search_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='search_history',
            name='ip',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='search_history',
            name='browser',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='search_history',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_search', to=settings.AUTH_USER_MODEL),
        ),
    ]