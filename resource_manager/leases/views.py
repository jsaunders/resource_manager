from django.views.generic import FormView
from django.views.generic import ListView

from resource_manager.leases.serializers import LeaseResourceSerializer
from .models import Resource


class ResourceListView(ListView):
    model = Resource

    def get_context_data(self, **kwargs):
        Resource.sync_resources_from_s3()
        serializer = LeaseResourceSerializer()
        context = super(ResourceListView, self).get_context_data()
        context['serializer']=serializer
        return context
