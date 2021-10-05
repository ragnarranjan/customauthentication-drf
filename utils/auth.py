from rest_framework import authentication
from rest_framework import exceptions
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from rest_framework import status, exceptions
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
import jwt
import json
from django.http import JsonResponse
import re
from django.urls import resolve
from rest_framework.response import Response
from django.contrib.auth.models import User
from social.settings import DB


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = {}
        key = "aaaa"
        users_collection = DB["users"]
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"]
            try:
                payload = jwt.decode(token,key )
                username = payload["username"]
                #try:
                    #user = User.objects.get(username=username)
                try:
                    usr_nm = users_collection.find_one({"username":username},{"_id":0})
                    print("4"*100,usr_nm)
                    user["username"] = usr_nm.get("username")
                    user["email"] = usr_nm.get("email")
                    user["name"] = usr_nm.get("name")                        
                except:
                    raise exceptions.AuthenticationFailed('No such user')
                        
                
            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('Invalid authorization token')
        else:
            raise exceptions.AuthenticationFailed('Invalid authorization token')

        return user, None


