import datetime
import math
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Amenities, Facilities, House

__all__ = (
    'HouseListTest',
)

User = get_user_model()


class HouseListTest(APITestCase):
    URL = '/house/'

    HOUSE_COUNT = 13
    PAGE_SIZE = 3

    AMENITIES_LIST = ['TV', '에어컨', '전자렌지', '커피포트', '컴퓨터', '공기청정기']
    FACILITIES_LIST = ['수영장', '엘리베이터', '세탁소', '노래방', '오락실', '온천']

    AMENITIES = [1, 2, 3, 4]
    FACILITIES = [1, 2, 3]

    DATA = {
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

    def setUp(self):
        test_user_data1 = {
            'username': 'test01@gmail.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'first_name': '수민',
            'last_name': '박',
            'phone_num': '010123456789',
        }
        test_user_data2 = {
            'username': 'test02@gmail.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'first_name': '보영',
            'last_name': '박',
            'phone_num': '01099874456',
        }
        self.user1 = User.objects.create_django_user(**test_user_data1)
        self.user2 = User.objects.create_django_user(**test_user_data2)

        [Amenities.objects.create(name=name) for name in self.AMENITIES_LIST]
        [Facilities.objects.create(name=name) for name in self.FACILITIES_LIST]

        for i in range(self.HOUSE_COUNT):
            self.DATA['host'] = self.user1 if i % 2 else self.user2

            house = House.objects.create(**self.DATA)

            for amenity in self.AMENITIES:
                house.amenities.add(amenity)

            for facility in self.FACILITIES:
                house.facilities.add(facility)

    def test_list_house(self):
        page_num = math.ceil(self.HOUSE_COUNT / self.PAGE_SIZE)

        for i in range(int(page_num)):
            response = self.client.get(self.URL, {'page': i + 1, 'page_size': self.PAGE_SIZE})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertIsNotNone(response.data['count'], 'count')
            self.assertEqual(response.data['count'], self.HOUSE_COUNT)

            if i < page_num - 1:
                self.assertIsNotNone(response.data['next'], 'next')
            if i > 0:
                self.assertIsNotNone(response.data['previous'], 'previous')

            results = response.data['results']

            for j in range(len(results)):
                house_result = results[j]
                self.assertEqual(house_result['pk'], ((i * self.PAGE_SIZE) + j) + 1)
                self.assertEqual(house_result['house_type'], self.DATA['house_type'])
                self.assertEqual(house_result['name'], self.DATA['name'])
                self.assertEqual(house_result['description'], self.DATA['description'])
                self.assertEqual(house_result['room'], self.DATA['room'])
                self.assertEqual(house_result['bed'], self.DATA['bed'])
                self.assertEqual(house_result['bathroom'], self.DATA['bathroom'])
                self.assertEqual(house_result['personnel'], self.DATA['personnel'])
                self.assertEqual(house_result['amenities'], self.AMENITIES)
                self.assertEqual(house_result['facilities'], self.FACILITIES)
                self.assertEqual(house_result['minimum_check_in_duration'], self.DATA['minimum_check_in_duration'])
                self.assertEqual(house_result['maximum_check_in_duration'], self.DATA['maximum_check_in_duration'])
                self.assertEqual(house_result['maximum_check_in_range'], self.DATA['maximum_check_in_range'])
                self.assertEqual(house_result['price_per_night'], self.DATA['price_per_night'])
                self.assertEqual(house_result['created_date'], datetime.date.today().strftime('%Y-%m-%d'))
                self.assertEqual(house_result['modified_date'], datetime.date.today().strftime('%Y-%m-%d'))
                self.assertEqual(house_result.get('host').get('pk'),
                                 self.user1.pk if ((i * self.PAGE_SIZE) + j) % 2 else self.user2.pk)
                self.assertEqual(house_result['country'], self.DATA['country'])
                self.assertEqual(house_result['city'], self.DATA['city'])
                self.assertEqual(house_result['district'], self.DATA['district'])
                self.assertEqual(house_result['dong'], self.DATA['dong'])
                self.assertEqual(house_result['address1'], self.DATA['address1'])
                self.assertEqual(house_result['address2'], self.DATA['address2'])
                self.assertEqual(house_result['latitude'], self.DATA['latitude'])
                self.assertEqual(house_result['longitude'], self.DATA['longitude'])

                house = House.objects.get(pk=house_result['pk'])
                self.assertEqual(house.pk, ((i * self.PAGE_SIZE) + j) + 1)
                self.assertEqual(house.house_type, self.DATA['house_type'])
                self.assertEqual(house.name, self.DATA['name'])
                self.assertEqual(house.description, self.DATA['description'])
                self.assertEqual(house.room, self.DATA['room'])
                self.assertEqual(house.bed, self.DATA['bed'])
                self.assertEqual(house.bathroom, self.DATA['bathroom'])
                self.assertEqual(house.personnel, self.DATA['personnel'])
                self.assertEqual(list(house.amenities.values_list('pk', flat=True)), self.AMENITIES)
                self.assertEqual(list(house.facilities.values_list('pk', flat=True)), self.FACILITIES)
                self.assertEqual(house.minimum_check_in_duration, self.DATA['minimum_check_in_duration'])
                self.assertEqual(house.maximum_check_in_duration, self.DATA['maximum_check_in_duration'])
                self.assertEqual(house.maximum_check_in_range, self.DATA['maximum_check_in_range'])
                self.assertEqual(house.price_per_night, self.DATA['price_per_night'])
                self.assertEqual(house.created_date, datetime.date.today())
                self.assertEqual(house.modified_date, datetime.date.today())
                self.assertEqual(house.host.pk,
                                 self.user1.pk if ((i * self.PAGE_SIZE) + j) % 2 else self.user2.pk)
                self.assertEqual(house.country, self.DATA['country'])
                self.assertEqual(house.city, self.DATA['city'])
                self.assertEqual(house.district, self.DATA['district'])
                self.assertEqual(house.dong, self.DATA['dong'])
                self.assertEqual(house.address1, self.DATA['address1'])
                self.assertEqual(house.address2, self.DATA['address2'])
                self.assertEqual(house.latitude, Decimal(self.DATA['latitude']))
                self.assertEqual(house.longitude, Decimal(self.DATA['longitude']))