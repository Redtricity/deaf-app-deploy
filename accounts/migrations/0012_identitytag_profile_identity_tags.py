# Generated by Django 5.1.5 on 2025-04-22 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_profile_sign_language_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdentityTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='identity_tags',
            field=models.ManyToManyField(blank=True, to='accounts.identitytag'),
        ),
    ]
