from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.status import *
from rest_framework.response import Response
from api.models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def pages(request):
    items = Item.objects.count()
    pages = items // 10
    if items % 10 != 0:
        pages += 1
    return Response({'pages': pages},
                    status=HTTP_200_OK)


class GetProviders(APIView):
    permission_classes = [IsAuthenticated]  # policy attribute
    renderer_classes = [JSONRenderer]  # policy attribute
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        providers = Provider.objects.all()
        response = [{'name': provider.name, 'email': provider.email, 'phone': provider.phone, 'address': provider.address} for provider in providers]
        return Response(response, status=HTTP_200_OK)


class GetItems(APIView):
    permission_classes = [IsAuthenticated]  # policy attribute
    renderer_classes = [JSONRenderer]  # policy attribute
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        items = Item.objects.all().order_by('category')
        response = [{'pk': item.pk, 'category': item.category.name, 'name': item.name, 'count': item.count, } for item in items]
        return Response(response, status=HTTP_200_OK)


class Batches(APIView):
    permission_classes = [IsAuthenticated]  # policy attribute
    renderer_classes = [JSONRenderer]  # policy attribute
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        batches = [str({'pk': batch.pk, 'date': batch.date.strftime("%B %d, %Y"), 'provider': batch.provider.name}) for batch in Batch.objects.all().order_by('pk')]
        return Response(batches, status=HTTP_200_OK)


class AddBatch(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        date = request.data['date'].split('.')
        date_formated = f'{date[2]}-{date[1]}-{date[0]}'
        new_object = Batch.objects.create(date=date_formated,
                             provider=Provider.objects.filter(name=request.data['provider']).get())
        new_object.save()
        return Response(status=HTTP_200_OK)


class AddProvider(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=50)

    def post(self, request):
        date = request.data['date'].split('.')
        date_formated = f'{date[2]}-{date[1]}-{date[0]}'
        new_object = Batch.objects.create(date=date_formated,
                             provider=Provider.objects.filter(name=request.data['provider']).get())
        new_object.save()
        return Response(status=HTTP_200_OK)


class GetOrders(APIView):
    permission_classes = [IsAuthenticated]  # policy attribute
    renderer_classes = [JSONRenderer]  # policy attribute
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        orders = [str({'pk': order.pk, 'date': 'потом', 'client': order.client.username}) for order in Order.objects.all().order_by('pk')]
        return Response(orders, status=HTTP_200_OK)



@api_view(['POST'])
def delete(self, pk):
    try:
        Batch.objects.filter(pk=pk).delete()
        return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_403_FORBIDDEN)

class ValidateToken(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        return Response(status=HTTP_200_OK)
