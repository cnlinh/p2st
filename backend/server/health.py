from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthCheck(APIView):
    def get(self, request, format=None):
        return Response({'status': 'healthy'}, status=status.HTTP_200_OK)
