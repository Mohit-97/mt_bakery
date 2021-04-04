from collections import OrderedDict

from django.contrib.auth.models import User
from django.contrib.auth import login

from rest_framework import generics, permissions, mixins, views
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from user.serializers import UserSerializer, CreateUserSerializer


class Welcome(views.APIView):
    def get(self, request):
        return Response({'message': 'Welcome'})


class RegisterAPI(generics.GenericAPIView):
    """
    User can register through this api
    """
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()
                                ).data,
            "token": token
        })


class LoginAPI(KnoxLoginView):
    """"""
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        data = super(LoginAPI, self).post(request, format=None).data

        #updating token
        token = "token " + data.get('token')
        data.update({'token': token})

        return Response({"data": data})


@api_view(('GET',))
def api_root(request, format=None):
    return Response(OrderedDict([
        ('User APIs', OrderedDict([
            ('register user', reverse('register', request=request, format=format)),
            ('login user', reverse('login', request=request, format=format)),
            ('logout user', reverse('logout', request=request, format=format)),
            ])
        ),
        ('Product APIs', OrderedDict([
            ('product-list', reverse('product-list', request=request, format=format)),
            ('product-detail', reverse('product-detail', request=request, format=format, args=[1]))
            ])
        ),
        ('Order APIs', OrderedDict([
            ('order-list', reverse('order', request=request, format=format)),
            ])
        )

    ]))
