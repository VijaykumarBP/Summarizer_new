# Generated by Django 3.2.12 on 2022-04-06 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prompt',
            name='article_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
