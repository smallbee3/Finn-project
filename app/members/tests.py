import random

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from rest_framework.test import APITestCase

from .apis import UserRetrieveUpdateDestroyAPIView, UserSerializer

User = get_user_model()


class UserSignupTest(APITestCase):

    def test_user_signup(self):
        """
        Method: POST
        일반회원이 회원가입 테스트
        :return:
        """
        test_user_info = {
            'username': 'test_user_02@gmail.com',
            'password': 'asdfqwer',
            'confirm_password': 'asdfqwer',
            'first_name': 'Park',
            'last_name': 'Boyoung',
            'phone_num': '010-1234-5678',
        }

        response = self.client.post(
            '/user/',
            test_user_info,
        )

        result = response.json()

        # status_code 확인
        self.assertEqual(response.status_code, 200)

        # Signup 요청의 내용과 response의 내용 일치 확인
        self.assertEqual(result['user']['username'], test_user_info['username'])
        self.assertEqual(result['user']['first_name'], test_user_info['first_name'])
        self.assertEqual(result['user']['last_name'], test_user_info['last_name'])
        self.assertEqual(result['user']['phone_num'], test_user_info['phone_num'])

        # user 객체가 정상적으로 생성되었는지 확인
        user = User.objects.get(username=test_user_info['username'])
        self.assertEqual(user.username, test_user_info['username'])
        self.assertEqual(user.first_name, test_user_info['first_name'])
        self.assertEqual(user.last_name, test_user_info['last_name'])
        self.assertEqual(user.phone_num, test_user_info['phone_num'])
        self.assertEqual(user.check_password(test_user_info['password']), True)
        self.assertEqual(user.is_email_user, True)
        self.assertEqual(user.is_facebook_user, False)
        self.assertEqual(user.is_host, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertIsNotNone(user.created_date)
        self.assertIsNotNone(user.modified_date)

        # host 전환 후 인증 되는지 검사
        user.is_host = True
        user.save()
        self.assertEqual(user, authenticate(
            username=test_user_info['username'],
            password=test_user_info['password'],
        ))

        # user 정보 출력해서 직접 확인
        print(UserSerializer(user).data)


class UserListTest(APITestCase):

    MODEL = User
    VIEW = UserRetrieveUpdateDestroyAPIView
    PATH = '/user/'
    PAGINATION_COUNT = 25

    def test_user_list_count(self):
        num = random.randrange(1, 30)
        # for i in range(num):
            # User.objects.create()

    def test_artist_list_pagination(self):
        pass


class UserLoginTest(APITestCase):

    def test_user_login(self):
        pass


class UserLogoutTest(APITestCase):

    def test_user_logout(self):
        pass


class UserDetailTest(APITestCase):

    def test_user_detail(self):
        pass


class UserDeleteTest(APITestCase):

    def test_user_delete(self):
        pass


class UserUpdateTest(APITestCase):

    def test_user_update(self):
        pass
