# Generated by Django 5.0.6 on 2024-07-03 22:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0013_postres_post_res'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='res',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_res', to='social.postres'),
        ),
    ]
