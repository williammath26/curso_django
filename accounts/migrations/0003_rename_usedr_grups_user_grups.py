# Generated by Django 4.2.4 on 2024-12-16 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_group_usedr_grups_group_permissions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usedr_Grups',
            new_name='User_Grups',
        ),
    ]