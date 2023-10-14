from django.test import TestCase,  Client
from .models import Item


# class ItemModelTests(TestCase):
#     def test_item_view_301(self):
#         client = Client()
#         response = self.client.get('/item',{},follow=True) 
#         self.assertIs(response.status_code, 301)