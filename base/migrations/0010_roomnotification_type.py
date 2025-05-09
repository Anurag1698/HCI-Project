# Generated by Django 5.2 on 2025-04-21 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_roomremovalnotice'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomnotification',
            name='type',
            field=models.CharField(choices=[('removed', 'Removed from room'), ('rejected', 'Join request rejected')], default='removed', max_length=10),
            preserve_default=False,
        ),
    ]
