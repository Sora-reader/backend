# Generated by Django 4.1.3 on 2022-12-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manga", "0010_alter_savelist_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="manga",
            name="popularity",
            field=models.IntegerField(default=0, verbose_name="Позиция в рейтинге"),
            preserve_default=False,
        ),
    ]