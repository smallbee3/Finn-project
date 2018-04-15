# Generated by Django 2.0.3 on 2018-04-15 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0003_auto_20180415_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseimage',
            name='house',
            field=models.ForeignKey(help_text='이미지와 연결된 숙소를 저장합니다.', on_delete=django.db.models.deletion.CASCADE, related_name='image', to='house.House', verbose_name='숙소'),
        ),
    ]
