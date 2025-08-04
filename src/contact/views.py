from rest_framework import viewsets, mixins
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer