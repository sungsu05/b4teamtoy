from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User


# 회원 가입 테스트
class SignupAPIViewTest(APITestCase):
    def test_singup(self):
        url = reverse("sign_up")
        user_data = {
            'nickname': 'son',
            'password': '123',
            'username': 'SungSuSon',
            'email': 'test@naver.com',
            'is_seller': True
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)

    # 회원 가입 실패
    def test_singup_fail(self):
        url = reverse("sign_up")
        user_data = {
            'nickname': 'son',
            'password': '123',
            'username': 'SungSuSon',

            'is_seller': False
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)

# 로그인 테스트
class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {
            'nickname': 'Rumor',
            'password': '123',
            'username': 'SungSuSon',
            'email': 'test@naver.com',
            'is_seller': True
        }

        # def create_user(self, email, username, nickname, is_seller, password=None):
        # 데이터 넘기는 순서 참고.
        self.user = User.objects.create_user('test@naver.com','SungSuSon','Rumor',True,'123')

    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'),self.data)
        # print(response.data["access"])
        self.assertEqual(response.status_code, 200)
        
        
# 회원 정보 수정 테스트
class UserAPIViewTest(APITestCase):
    def setUp(self):
        self.data = {
            'nickname': 'Rumor',
            'password': '123',
            'username': 'SungSuSon',
            'email': 'test@naver.com',
            'is_seller': True
        }

        # def create_user(self, email, username, nickname, is_seller, password=None):
        # 데이터 넘기는 순서 참고.
        self.user = User.objects.create_user('test@naver.com','SungSuSon','Rumor',True,'123')
        self.response = self.client.post(reverse('token_obtain_pair'),self.data)

    # # 회원 정보 수정
    # def test_update(self):
    #     token = self.response.data["access"]
    #     url = reverse('user_view',args=[self.user.id])
    #     # url = reverse('user_view')
    #     self.data = {
    #         'nickname': '초능력 맛',
    #         'password': '12345',
    #         'username': '손성수',
    #         'email': 'rumor@naver.com',
    #         'is_seller': 'S'
    #     }
    #     response = self.client.put(
    #         path = url,
    #         data = self.data,
    #         content_type ="application/json",
    #         HTTP_AUTHORIZATION = f"Bearer {token}"
    #     )
    #     print(response)
    #     self.assertEqual(response.status_code,200)
