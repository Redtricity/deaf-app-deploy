# Generated by Django 5.1.5 on 2025-04-22 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sign_language_preference',
            field=models.CharField(choices=[('bsl', 'British Sign Language'), ('asl', 'American Sign Language'), ('other', 'Other')], default='bsl', max_length=10),
        ),
    ]
