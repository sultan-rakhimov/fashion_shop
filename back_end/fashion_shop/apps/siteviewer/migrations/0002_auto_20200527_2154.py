# Generated by Django 3.0.6 on 2020-05-27 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteviewer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category',
        ),
        migrations.RemoveField(
            model_name='color',
            name='color',
        ),
        migrations.RemoveField(
            model_name='size',
            name='size',
        ),
        migrations.AddField(
            model_name='category',
            name='title',
            field=models.CharField(choices=[('W', 'Winter'), ('Sp', 'Spring'), ('Sm', 'Summer'), ('F', 'Fall'), ('W-F', 'Winter-Fall'), ('Sp-Sm', 'Spring-Summer')], default='asas', max_length=128, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='title',
            field=models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('black', 'Black'), ('white', 'White')], default='sasa', max_length=128, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='size',
            name='title',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')], default='ff', max_length=128, verbose_name='Title'),
            preserve_default=False,
        ),
    ]