from django.test import TestCase
from.views import xyz

def test_profile(self):
    abc = self.client.get('/about/')
    self.assertEqual(abc.status_code,200)
    

