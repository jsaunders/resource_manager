from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from resource_manager.leases.models import Resource
from resource_manager.leases.serializers import LeaseResourceSerializer


class LeaseResourceView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)




    def post(self,request, pk, format=None):
        serializer = LeaseResourceSerializer(data=request.data)
        if serializer.is_valid():
            pass
            user = request.user
            try:
                resource = Resource.objects.get(pk=pk)
                resource.lease_resource(user,serializer.data.get('duration'))
            except Resource.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

