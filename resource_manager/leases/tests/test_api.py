from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from test_plus import TestCase

from resource_manager.leases.api import LeaseResourceView
from resource_manager.leases.models import Resource


class TestLeases(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_lease_endpoint_invalid(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/api/v1/lease-resource/832323/',{'duration':100},format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_lease_endpoint_authorization(self):
        client = APIClient()
        Resource.sync_resources_from_s3()
        resource = Resource.objects.first()
        response = client.post('/api/v1/lease-resource/{0}/'.format(resource.pk),{'duration':100},format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_lease_endpoint_simple(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        Resource.sync_resources_from_s3()
        resource = Resource.objects.first()
        self.assertTrue(resource.available)
        response = client.post('/api/v1/lease-resource/{0}/'.format(resource.pk),{'duration':100},format='json')
        self.assertEqual(response.status_code,status.HTTP_202_ACCEPTED)
        self.assertFalse(resource.available)
        resource = Resource.objects.first()
        resource.end_lease()


    def test_lease_end(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        Resource.sync_resources_from_s3()
        resource = Resource.objects.first()
        self.assertTrue(resource.available)
        response = client.post('/api/v1/lease-resource/{0}/'.format(resource.pk), {'duration': 100}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(resource.available)
        resource = Resource.objects.first()
        with open(resource.path, "a") as f:
            f.write("new line\n")
        resource.end_lease()






