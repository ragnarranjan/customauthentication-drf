from rest_framework.views import APIView
from utils.auth import CustomAuthentication

class AuthAPIView(APIView):
    authentication_classes = [CustomAuthentication, ]