from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_remove_movie_trailer_url_movie_trailer'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
