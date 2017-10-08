from django.contrib.auth.models import User
from django.db.transaction import atomic
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework import filters

from transfers.permissions import CreateOnly
from transfers.serializers import UserSerializer, TransferSerializer
from transfers.transfer import TransferService, TransferException


def index(request):
    return render(request, 'index.html', {})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username', '^email', '^first_name', '^last_name')

    serializer_class = UserSerializer
    queryset = User.objects.all()


class TransferViewSet(viewsets.ViewSet):
    serializer_class = TransferSerializer
    permission_classes = (CreateOnly,)

    @atomic()
    def create(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            service = TransferService()
            try:
                from_profile, inn_profiles = service.make_transfer(serializer.validated_data)
            except TransferException as e:
                return Response({'non_field_errors': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

            resp_data = {
                'msg': 'Transfer successful',
                'from': from_profile.user.username,
                'to': ', '.join([inn_profile.user.username for inn_profile in inn_profiles]),
                'amount': serializer.create(serializer.validated_data).amount
            }
            return Response(resp_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
