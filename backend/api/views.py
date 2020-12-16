from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions, status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Article
from cert.models import CustomUser
