# Generated by Django 3.1 on 2023-08-09 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_partbelongs'),
        ('store', '0003_auto_20230809_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='belongs_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.partbelongs'),
        ),
    ]
