from .models import Contact, About, Goal
from rest_framework import generics
from .serializers import ContactSerializer, AboutSerialkizer, GoalSerializer


class ContactAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class AboutAPIView(generics.ListAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerialkizer


class GoalAPIView(generics.ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
