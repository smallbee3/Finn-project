from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.test import APITestCase

__all__ = (
    'UserSignupTest',
)

User = get_user_model()


class UserSignupTest(APITestCase):
    URL = '/user/'
    USERNAME = 'test@gmail.com'
    PASSWORD = 'testpassword'
    FIRST_NAME = '수민'
    LAST_NAME = '박'
    PHONE_NUM = '01012345567'

    def test_signup(self):
        # 유저 만듬
        data = {
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'confirm_password': self.PASSWORD,
            'first_name': self.FIRST_NAME,
            'last_name': self.LAST_NAME,
            'phone_num': self.PHONE_NUM,
        }
        response = self.client.post(self.URL, data)
        # signup 결과 response 테스트

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['token'], Token.objects.get(user=User.objects.first()).key)

        self.assertIsNotNone(response.data['user'], 'user')
        user_data = response.data['user']
        self.assertEqual(user_data['username'], self.USERNAME)
        self.assertEqual(user_data['email'], self.USERNAME)
        self.assertEqual(user_data['first_name'], self.FIRST_NAME)
        self.assertEqual(user_data['last_name'], self.LAST_NAME)
        self.assertEqual(user_data['phone_num'], self.PHONE_NUM)

        # authenticate를 사용해 실제 데이터베이스에 생성되었는지 확인,
        # 생성된 유저의 값을 테스트
        user = authenticate(username=self.USERNAME, password=self.PASSWORD)

        self.assertEqual(user.pk, user_data['pk'])
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.username, user_data['email'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])
        self.assertEqual(user.phone_num, user_data['phone_num'])
        self.assertEqual(user.check_password(data['password']), True)
        self.assertEqual(user.is_email_user, True)
        self.assertEqual(user.is_facebook_user, False)
        self.assertEqual(user.is_host, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertIsNotNone(user.created_date)
        self.assertIsNotNone(user.modified_date)
