from django.shortcuts import render
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.

class GetToplevelTopicView(APIView):
    def get(self,request):
        pass
        

class GetMidlevelTopicView(APIView):
    def get(self,request):
        pass

class GetLowlevelTopicView(APIView):
    def get(self,request):
        pass

class GetProductTopicView(APIView):
    def get(self,request):
        pass