import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Amenities, Facilities, House

__all__ = (
    'HouseUpdateTest',
)

User = get_user_model()


class HouseUpdateTest(APITestCase):
    URL = '/house/'
    HOUSE_PK = 1

    AMENITIES_LIST = ['TV', '에어컨', '전자렌지', '커피포트', '컴퓨터', '공기청정기']
    FACILITIES_LIST = ['수영장', '엘리베이터', '세탁소', '노래방', '오락실', '온천']

    BASE_AMENITIES = [1, 2, 3, 4]
    BASE_FACILITIES = [1, 2, 3]

    BASE_DATA = {
        'house_type': House.HOUSE_TYPE_HOUSING,
        'name': '우리집',
        'description': '테스트용 집입니다.',
        'room': 1,
        'bed': 2,
        'bathroom': 2,
        'personnel': 3,
        'minimum_check_in_duration': 1,
        'maximum_check_in_duration': 3,
        'maximum_check_in_range': 3,
        'price_per_night': 100000,
        'country': '대한민국',
        'city': '사랑시',
        'district': '고백구',
        'dong': '행복동',
        'address1': '777-1',
        'address2': '희망빌라 2동 301호',
        'latitude': '12.1234567',
        'longitude': '123.1234567',
    }

    UPDATE_AMENITIES = []
    UPDATE_FACILITIES = [1, ]

    UPDATE_DATA = {
        'house_type': House.HOUSE_TYPE_APARTMENT,
        'name': '우리집',
        'description': '테스트용 집입니다.',
        'room': 1,
        'bed': 2,
        'bathroom': 2,
        'personnel': 3,
        'amenities': UPDATE_AMENITIES,
        'facilities': UPDATE_FACILITIES,
        'minimum_check_in_duration': 1,
        'maximum_check_in_duration': 3,
        'maximum_check_in_range': 3,
        'price_per_night': 100000,
        'country': '대한민국',
        'city': '사랑시',
        'district': '고백구',
        'dong': '행복동',
        'address1': '777-1',
        'address2': '희망빌라 2동 301호',
        'latitude': '12.1234567',
        'longitude': '123.1234567',
    }

    def setUp(self):
        test_user_data = {
            'username': 'test01@gmail.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'first_name': '수민',
            'last_name': '박',
            'phone_num': '010123456789',
        }
        self.user = User.objects.create_django_user(**test_user_data)

        [Amenities.objects.create(name=name) for name in self.AMENITIES_LIST]
        [Facilities.objects.create(name=name) for name in self.FACILITIES_LIST]

        self.BASE_DATA['host'] = self.user

        house = House.objects.create(**self.BASE_DATA)

        self.user.is_host = True
        self.user.save()

        for amenity in self.BASE_AMENITIES:
            house.amenities.add(amenity)

        for facility in self.BASE_FACILITIES:
            house.facilities.add(facility)

        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
        )

    def test_update_house(self):
        response = self.client.put(self.URL + f'{self.HOUSE_PK}/', self.UPDATE_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['house_type'], self.UPDATE_DATA['house_type'])
        self.assertEqual(response.data['name'], self.UPDATE_DATA['name'])
        self.assertEqual(response.data['description'], self.UPDATE_DATA['description'])
        self.assertEqual(response.data['room'], self.UPDATE_DATA['room'])
        self.assertEqual(response.data['bed'], self.UPDATE_DATA['bed'])
        self.assertEqual(response.data['bathroom'], self.UPDATE_DATA['bathroom'])
        self.assertEqual(response.data['personnel'], self.UPDATE_DATA['personnel'])
        self.assertEqual(response.data['amenities'], self.UPDATE_DATA['amenities'])
        self.assertEqual(response.data['facilities'], self.UPDATE_DATA['facilities'])
        self.assertEqual(response.data['minimum_check_in_duration'], self.UPDATE_DATA['minimum_check_in_duration'])
        self.assertEqual(response.data['maximum_check_in_duration'], self.UPDATE_DATA['maximum_check_in_duration'])
        self.assertEqual(response.data['maximum_check_in_range'], self.UPDATE_DATA['maximum_check_in_range'])
        self.assertEqual(response.data['price_per_night'], self.UPDATE_DATA['price_per_night'])
        self.assertEqual(response.data['created_date'], datetime.date.today().strftime('%Y-%m-%d'))
        self.assertEqual(response.data['modified_date'], datetime.date.today().strftime('%Y-%m-%d'))
        self.assertEqual(response.data['host']['pk'], self.user.pk)
        self.assertEqual(response.data['country'], self.UPDATE_DATA['country'])
        self.assertEqual(response.data['city'], self.UPDATE_DATA['city'])
        self.assertEqual(response.data['district'], self.UPDATE_DATA['district'])
        self.assertEqual(response.data['dong'], self.UPDATE_DATA['dong'])
        self.assertEqual(response.data['address1'], self.UPDATE_DATA['address1'])
        self.assertEqual(response.data['address2'], self.UPDATE_DATA['address2'])
        self.assertEqual(response.data['latitude'], self.UPDATE_DATA['latitude'])
        self.assertEqual(response.data['longitude'], self.UPDATE_DATA['longitude'])

        house = House.objects.get(pk=response.data['pk'])
        self.assertEqual(house.house_type, self.UPDATE_DATA['house_type'])
        self.assertEqual(house.name, self.UPDATE_DATA['name'])
        self.assertEqual(house.description, self.UPDATE_DATA['description'])
        self.assertEqual(house.room, self.UPDATE_DATA['room'])
        self.assertEqual(house.bed, self.UPDATE_DATA['bed'])
        self.assertEqual(house.bathroom, self.UPDATE_DATA['bathroom'])
        self.assertEqual(house.personnel, self.UPDATE_DATA['personnel'])
        self.assertEqual(list(house.amenities.values_list('pk', flat=True)), self.UPDATE_DATA['amenities'])
        self.assertEqual(list(house.facilities.values_list('pk', flat=True)), self.UPDATE_DATA['facilities'])
        self.assertEqual(house.minimum_check_in_duration, self.UPDATE_DATA['minimum_check_in_duration'])
        self.assertEqual(house.maximum_check_in_duration, self.UPDATE_DATA['maximum_check_in_duration'])
        self.assertEqual(house.maximum_check_in_range, self.UPDATE_DATA['maximum_check_in_range'])
        self.assertEqual(house.price_per_night, self.UPDATE_DATA['price_per_night'])
        self.assertEqual(house.created_date, datetime.date.today())
        self.assertEqual(house.modified_date, datetime.date.today())
        self.assertEqual(house.host.pk, self.user.pk)
        self.assertEqual(house.host.is_host, True)
        self.assertEqual(house.country, self.UPDATE_DATA['country'])
        self.assertEqual(house.city, self.UPDATE_DATA['city'])
        self.assertEqual(house.district, self.UPDATE_DATA['district'])
        self.assertEqual(house.dong, self.UPDATE_DATA['dong'])
        self.assertEqual(house.address1, self.UPDATE_DATA['address1'])
        self.assertEqual(house.address2, self.UPDATE_DATA['address2'])
        self.assertEqual(house.latitude, Decimal(self.UPDATE_DATA['latitude']))
        self.assertEqual(house.longitude, Decimal(self.UPDATE_DATA['longitude']))