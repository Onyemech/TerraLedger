from rest_framework.test import APITestCase
from rest_framework import status

class LandTests(APITestCase):
    def test_that_land_can_be_created(self):
        data = {
            'name': 'Plot A',
            'address': '123 Main St',
            'coordinates': 'lat:123,long:456',
            'pdf_data': 'sample pdf content',
            'issuer_id': 'registry123'
        }
        response = self.client.post('/api/lands/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_that_land_can_update_land(self):
        data = {
            'name': 'Plot A Updated',
            'address': '456 Main St',
            'coordinates': 'lat:124,long:457',
            'pdf_data': 'updated pdf content',
            'issuer_id': 'registry123'
        }
        response = self.client.put('/api/lands/0x123/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])