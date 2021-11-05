from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0024_auto_20210930_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manga',
            name='updated_chapters',
        ),
        migrations.AddField(
            model_name='chapter',
            name='manga',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parse.manga'),
        ),
        # move everything from M2M to column
        migrations.RunSQL("""
        UPDATE parse_chapter
            SET manga_id = pmc.manga_id
            FROM parse_manga_chapters AS pmc
                WHERE parse_chapter.id = pmc.chapter_id;
        """),
        migrations.RemoveField(
            model_name='manga',
            name='chapters',
        ),
        migrations.AlterField(
            model_name='chapter',
            name='manga',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='parse.manga'),
        ),
    ]
