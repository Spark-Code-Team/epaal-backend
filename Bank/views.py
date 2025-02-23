from django.shortcuts import render
from rest_framework.views import APIView
from .models import Facility
from .serializers import FacilitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class GetAllFacilityView(APIView):
    serializer_class = FacilitySerializer
    def get(self, request):
        facilities = Facility.objects.all()
        serializer = FacilitySerializer(facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)