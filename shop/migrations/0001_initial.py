# Generated by Django 4.0.5 on 2022-06-08 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Category name')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default='null', unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Model')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('producer', models.CharField(max_length=64, verbose_name='Producer')),
                ('producerCountry', models.CharField(max_length=64, verbose_name='Producer country')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Category')),
            ],
        ),
    ]
