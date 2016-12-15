import datetime
import os
import stat

import pytz
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
from django.db import IntegrityError
from django.db import models

# Create your models here.

RESOURCE_TYPES = (
    ('file','file'),
    ('server','server')
)


class Lease(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    active = models.BooleanField(default=True)
    resource = models.ForeignKey('Resource')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class Resource(models.Model):
    """
    A Resource represents any type of resource that can be leased
    """
    name = models.CharField(max_length=100, default="Default Name")
    leasers = models.ManyToManyField(settings.AUTH_USER_MODEL, through=Lease)
    type = models.CharField(max_length=50, choices=RESOURCE_TYPES, default='file')
    path = models.CharField(max_length=200)
    key = models.CharField(max_length=200,unique=True)

    def assign_user(self, user, duration):
        """
        Assigns a user object to this resource for length of duration
        :param user:
        :param duration:
        :return:
        """
        now = pytz.utc.localize(datetime.datetime.utcnow())
        difference = datetime.timedelta(minutes=duration)
        end_time = now + difference
        Lease.objects.create(
            start_time=now,
            end_time=end_time,
            resource=self,
            user=user)

    @property
    def available(self):
        """
        Determines if resource is available by checking if there are any active leases that have an association with it
        :return bool:
        """
        leases = Lease.objects.filter(active=True,resource=self)
        return len(leases)==0

    @property
    def booked_by(self):
        """
        if this resource is booked returns leasees username,
        if no one has booked it returns 'Available'
        :return:
        """
        try:
            lease = Lease.objects.get(active=True,resource=self)
            return lease.user.username
        except Lease.DoesNotExist:
            return 'Available'

    @property
    #todo: make work for distributed system, i.e handle multiple users
    def next_time_available(self):
        """
        if this resource is booked returns next time available,
        if no one has booked it returns 'Now'
        Assumes single user system for this trivial implementation
        :return:
        """
        try:
            lease = Lease.objects.get(active=True,resource=self)
            return lease.end_time
        except Lease.DoesNotExist:
            return 'Now'

    @staticmethod
    def list_resources_from_s3():
        """
        List resources in an s3 bucket
        bucket_name, aws access key, and secret access key are located in the settings file
        :return [key]:
        """
        conn = S3Connection(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_S3_BUCKET_NAME)
        keys = bucket.get_all_keys()
        return [key.key for key in keys]

    @staticmethod
    #todo: add meaningful return
    def sync_resources_from_s3():
        """
        Syncs local databse to ensure anything found in s3 bucket has a database object created for it.
        Reverse is not true!
        """
        keys = Resource.list_resources_from_s3()
        for key in keys:
            try:
                Resource.objects.get(key=key)
            except Resource.DoesNotExist:
                Resource.objects.create(name=key,key=key,path='/')

    #todo: add meaningful return
    def save_resource_to_s3(self):
        """
        Save this local resource to s3 bucket
        """
        conn = S3Connection(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_S3_BUCKET_NAME)
        k = Key(bucket)
        k.key=self.key
        k.set_contents_from_filename(self.path)

    #todo: add meaningful return
    def end_lease(self):
        """
        Ends the lease of an object. This:
         1. saves the resource to the s3 bucket
         2. sets lease object active status to False
         3. deletes file from host os
        """
        self.save_resource_to_s3()
        lease = Lease.objects.get(active=True,resource=self)
        lease.active=False
        lease.save()
        os.remove(self.path)

    #todo: add meaningful return
    def lease_resource(self,user,duration):
        """
        Leases *this* resource to 'user' for 'duration' minutes
        This:
        1. Saves file to location
        2. Modifies the permissions so it is editable by all users
        3. Calls assign user to make database object change
        :param user:
        :param duration:
        """
        conn = S3Connection(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_S3_BUCKET_NAME)
        target_filename = '/shared/{0}'.format(self.key)
        k = Key(bucket)
        k.key = self.key
        k.get_contents_to_filename(target_filename)
        self.path = target_filename
        self.save()
        self.make_file_permissions_editable()
        self.assign_user(user,duration)

    def make_file_permissions_editable(self):
        os.chmod(self.path, 0o777)


    @staticmethod
    def list_permissions_of_file(path):
        """
        prints permissions in 3 digit mode format, will behave differently for symlinks vs files
        :param path:
        :return 3 digit int:
        """
        return oct(stat.S_IMODE(os.stat(path).st_mode))[2:]







    def __str__(self):
        return self.name
