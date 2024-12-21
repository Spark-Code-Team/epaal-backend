from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import All_ToplevelSerializer
from .models import ToplevelTopic
# Create your views here.

class ALLCategory(APIView):
    def get(self, request):
        if ToplevelTopic.objects.filter().exists():
            ser_data=All_ToplevelSerializer(instance=ToplevelTopic.objects.filter(),many=True)
            return Response({"toplevel_topic":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any top level topic"},status=status.HTTP_204_NO_CONTENT)