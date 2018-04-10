# Generated by Django 2.0.3 on 2018-04-10 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 까지의 물건의 이름을 저장 합니다.', max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': '편의 물품',
            },
        ),
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='100자 까지의 물건의 이름을 저장 합니다.', max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': '편의 시설',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_type', models.CharField(choices=[('AP', '아파트'), ('HO', '주택'), ('OR', '원룸')], default='HO', help_text='숙소를 선택 하세요. 디비에는 AP HO OR 등으로 저장.(기본값은 주택)', max_length=2, verbose_name='숙소 타입')),
                ('name', models.CharField(help_text='숙소의 이름을 입력하세요.', max_length=100, verbose_name='숙소 이름')),
                ('description', models.TextField(help_text='숙소를 설명 하세요.', verbose_name='숙소 설명')),
                ('room', models.PositiveSmallIntegerField(help_text='방 수를 입력 하세요.', verbose_name='방 수')),
                ('bed', models.PositiveSmallIntegerField(help_text='침대 수를 입력 하세요.', verbose_name='침대 수')),
                ('bathroom', models.PositiveSmallIntegerField(help_text='욕실 수를 입력 하세요.', verbose_name='욕실 수')),
                ('personnel', models.PositiveSmallIntegerField(help_text='숙박 인원 입력 하세요.', verbose_name='숙박 인원')),
                ('minimum_check_in_duration', models.PositiveSmallIntegerField(help_text='체크인 할 수 있는 최소 기간을 입력 하세요.', verbose_name='최소 체크인 기간')),
                ('maximum_check_in_duration', models.PositiveSmallIntegerField(help_text='체크인 할 수 있는 최대 기간을 입력 하세요.', verbose_name='최대 체크인 기간')),
                ('maximum_check_in_range', models.PositiveSmallIntegerField(help_text='오늘을 기준으로 체크인이 가능한 달 수 적어주세요', verbose_name='체크인 가능한 한계 시간')),
                ('price_per_night', models.PositiveSmallIntegerField(help_text='하루 요금을 적어 주세요.', verbose_name='하루 요금')),
                ('created_date', models.DateField(auto_now_add=True, help_text='날짜로 입력 가능 합니다.(기본값은 오늘)', verbose_name='등록일')),
                ('modified_date', models.DateField(auto_now=True, help_text='날짜로 입력 가능 합니다.(기본값은 오늘)', verbose_name='수정일')),
                ('country', models.CharField(blank=True, help_text='특별시/광역시/도 을 입력 하세요 (서울특별시)', max_length=100, verbose_name='국가')),
                ('city', models.CharField(blank=True, help_text='특별시/광역시/도 을 입력 하세요 (서울특별시)', max_length=100, verbose_name='시/도')),
                ('district', models.CharField(blank=True, help_text='시/군/구 를 입력 하세요 (관악구)', max_length=100, verbose_name='시/군/구')),
                ('dong', models.CharField(blank=True, help_text='상세 주소를 입력 하세요 (신림동)', max_length=100, verbose_name='동/읍/면')),
                ('address1', models.CharField(blank=True, help_text='상세 주소1을 입력 하세요 (790-2)', max_length=100, verbose_name='상세 주소1')),
                ('address2', models.CharField(blank=True, help_text='상세 주소2를 입력 하세요 (희망빌라 2차 201호)', max_length=100, verbose_name='상세 주소2')),
                ('latitude', models.DecimalField(decimal_places=7, help_text='위도를 소수점(7자리) 입력 가능 (xx.1234567)', max_digits=9, verbose_name='위도')),
                ('longitude', models.DecimalField(decimal_places=7, help_text='경도를 소수점(7자리) 입력 가능 (xxx.1234567)', max_digits=10, verbose_name='경도')),
                ('amenities', models.ManyToManyField(blank=True, help_text='편의 물품의 종류를 선택하세요.', related_name='houses_with_amenities', to='house.Amenities', verbose_name='편의 물품')),
                ('facilities', models.ManyToManyField(blank=True, help_text='편의 시설을 선택하세요.', related_name='houses_with_facilities', to='house.Facilities', verbose_name='편의 시설')),
                ('host', models.ForeignKey(help_text='숙소를 등록하는 호스트입니다.', on_delete=django.db.models.deletion.CASCADE, related_name='houses_with_host', to=settings.AUTH_USER_MODEL, verbose_name='호스트')),
            ],
            options={
                'verbose_name_plural': '숙소',
            },
        ),
        migrations.CreateModel(
            name='HouseImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='숙소와 연결된 이미지를 저장합니다.', upload_to='house', verbose_name='숙소 이미지')),
                ('kind', models.CharField(choices=[('IN', 'inner'), ('OU', 'outer')], default='IN', help_text='숙소 안 이미지 인지 바깥 이미지 인지 저장', max_length=2, verbose_name='이미지 타입')),
                ('house', models.ForeignKey(help_text='이미지와 연결된 숙소를 저장합니다.', on_delete=django.db.models.deletion.CASCADE, related_name='house_images', to='house.House', verbose_name='숙소')),
            ],
            options={
                'verbose_name_plural': '숙소 이미지들',
            },
        ),
    ]
