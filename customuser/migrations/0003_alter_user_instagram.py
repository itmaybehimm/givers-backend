# Generated by Django 3.2.4 on 2021-06-28 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0002_alter_user_instagram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='instagram',
            field=models.URLField(blank=True, default='www.fb.com', max_length=255, null=True),
        ),
    ]