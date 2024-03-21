from django.db import migrations, models
from django.utils.text import slugify

class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0004_alter_category_options'),
    ]

    def generate_category_slug(apps, schema_editor):
        Category = apps.get_model('finalapp', 'Category')
        for category in Category.objects.all():
            category.slug = slugify(category.name)
            category.save()

    def generate_movie_slug(apps, schema_editor):
        Movie = apps.get_model('finalapp', 'Movie')
        for movie in Movie.objects.all():
            movie.slug = slugify(movie.title)
            movie.save()

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=250, unique=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='created',
            field=models.DateField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(default='', max_length=250, unique=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.RunPython(generate_category_slug),
        migrations.RunPython(generate_movie_slug),
    ]
