# Generated by Django 2.2.14 on 2020-08-06 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200806_1539'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='experirence',
            new_name='experience',
        ),
        migrations.RenameField(
            model_name='experience',
            old_name='experirence_date_end',
            new_name='experience_date_end',
        ),
        migrations.RenameField(
            model_name='experience',
            old_name='experirence_date_start',
            new_name='experience_date_start',
        ),
        migrations.RenameField(
            model_name='experience',
            old_name='experirence_text',
            new_name='experience_text',
        ),
        migrations.RenameField(
            model_name='experience',
            old_name='experirence_title',
            new_name='experience_title',
        ),
    ]
