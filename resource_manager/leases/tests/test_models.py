import datetime

import pytz
from test_plus.test import TestCase

from resource_manager.leases.models import Resource, Lease


class TestLeases(TestCase):
    """Test Leases and Resources."""

    def setUp(self):
        self.resource = Resource.objects.create(name="Resource 1")
        self.user = self.make_user()

    def test_resource_exists(self):
        self.assertEqual(1, len(Resource.objects.all()))

    def test_resource_default_availability(self):
        self.assertTrue(self.resource.available)

    def test_resource_str_function(self):
        self.assertEqual(str(self.resource),self.resource.name)

    def test_resource_booking(self):
        self.assertTrue(self.resource.available)
        Lease.objects.create(
            resource=self.resource,
            user=self.user,
            start_time=pytz.utc.localize(datetime.datetime.utcnow()),
            end_time=pytz.utc.localize(datetime.datetime.utcnow())
        )
        self.assertFalse(self.resource.available)

    def test_resource_booked_by(self):
        self.assertTrue(self.resource.available)
        Lease.objects.create(
            resource=self.resource,
            user=self.user,
            start_time=pytz.utc.localize(datetime.datetime.utcnow()),
            end_time=pytz.utc.localize(datetime.datetime.utcnow())
        )
        self.assertFalse(self.resource.available)
        self.assertEqual(self.user.username,self.resource.booked_by)

    def test_available_resource_booked_by(self):
        self.assertTrue(self.resource.available)
        self.assertEqual("Available",self.resource.booked_by)

    def test_available_resource_next_available_time(self):
        self.assertTrue(self.resource.available)
        self.assertEqual("Now",self.resource.next_time_available)

    def test_resource_next_available_time(self):
        self.assertTrue(self.resource.available)
        end_time = pytz.utc.localize(datetime.datetime.utcnow())
        Lease.objects.create(
            resource=self.resource,
            user=self.user,
            start_time=pytz.utc.localize(datetime.datetime.utcnow()),
            end_time=end_time
        )
        self.assertEqual(end_time,self.resource.next_time_available)

    def test_resource_assign_user_method(self):
        self.assertTrue(self.resource.available)
        self.resource.assign_user(self.user,90)
        self.assertFalse(self.resource.available)





