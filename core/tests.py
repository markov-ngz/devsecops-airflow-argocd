from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import override_settings
# Create your tests here.

# @override_settings(
#     ACCOUNT_SIGNUP_FORM_CLASS=None,
#     ACCOUNT_EMAIL_SUBJECT_PREFIX=None,
#     ACCOUNT_ADAPTER="allauth.account.adapter.DefaultAccountAdapter",
# )
class TestCore(TestCase):
    

    def test_index_view_status_code_200(self):
        client = Client()
        response = self.client.get('/')
        self.assertIs(response.status_code, 200)

    def test_admin_view_status_code_200(self):
        client = Client()
        response = self.client.get('/admin',{},follow=True)
        self.assertIs(response.status_code, 200)
    
    def test_signup_view_status_code_200(self):
        client = Client()
        response = self.client.get('/accounts/signup',{},follow=True)
        self.assertIs(response.status_code, 200)

    # def test_login_view_status_code_200(self):
    #     client = Client()
    #     response = self.client.get('/accounts/login/')
    #     self.assertIs(response.status_code, 200)

    # bug  : customize login view form to enable test ? 
    # import allauth ? ? 