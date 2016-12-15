from boto.s3.connection import S3Connection
from django.conf import settings
from test_plus.test import TestCase

from resource_manager.leases.models import Resource


class TestS3Operations(TestCase):

    def setUp(self):
        self.conn = S3Connection(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY)


    # def test_list_resources(self):
    #     keys = Resource.list_resources_from_s3()
    #     for key in keys:
            # print(key)

    # def test_save_contents(self):
    #     keys = Resource.list_resources_from_s3()
    #     filename = Resource.lease_resource_with_key(keys[0])
    #     print(Resource.list_permissions_of_file(filename))
