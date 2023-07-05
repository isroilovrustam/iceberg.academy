from rest_framework import serializers
from .models import Contact, About, Goal


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'phone']


class AboutSerialkizer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['title', 'image_path', 'body']


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['icon_path', 'title', 'body']
