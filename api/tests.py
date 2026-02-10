from django.test import TestCase
from .models import CustomUser,RepairJob
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserRipairJobTestCase(TestCase):
   class UserRipairJobTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.creator = CustomUser.objects.create_user(
            username='user5',
            email='user5@test.com',
            password='pass@123'
        )

        cls.engineer = CustomUser.objects.create_user(
            username='engineer1',
            email='engineer1@test.com',
            password='pass@123'
        )

        cls.customer = CustomUser.objects.create_user(
            username='user6',
            email='user6@test.com',
            password='pass@123'
        )

        RepairJob.objects.create(
            customer_name=cls.customer,
            customer_phome=12041404152,
            address='cidco',
            device_type='laptop',
            device_brand='msi',
            device_model='model14',
            serial_number=2456454214,
            problem_description='screen',
            assigned_engineer=cls.engineer,
            created_by=cls.creator
        )

       
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = CustomUser.objects.get(username='user2')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders'))

        assert response.status_code == status.HTTP_200_OK
        jobs = response.json()
        self.assertTrue(all(RepairJob['user'] == user.id for order in jobs))

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-job'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)