from rest_framework import generics
from .models import Oda
from .serializers import OdaSerializer


class OdaList(generics.ListCreateAPIView):
    queryset = Oda.objects.all().order_by('-muda')
    serializer_class = OdaSerializer