# Generated by Django 3.1 on 2023-08-15 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20230815_1048'),
        ('carts', '0003_cartitem_variations'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]