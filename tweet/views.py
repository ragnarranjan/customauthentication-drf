from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework .response import Response
from rest_framework import status
import jwt 
from django.contrib.auth import authenticate
from tweet import models
from django.views import View
from django.contrib.auth.models import User
from .serializers import PostSerializers
from .models import Post, Like , Comment
from django.core.exceptions import ObjectDoesNotExist
from social.settings import DB



key = "aaaa"
class Login(APIView):

    def get(self,request):
        pass

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username,password)

        users_collection = DB["users"]
        user_name_password = users_collection.find_one({"username":username,"password":password })
        
        if user_name_password is not None:
            payload = {
            "username" : username,
            "password" : password
            }
            encoded_jwt = jwt.encode(payload, key)
            print(encoded_jwt)
            data = {
                "message":"signed in successfuly",
                "username":user_name_password.get("username"),
                "password":user_name_password.get("password"),
                "token":encoded_jwt,
                "success":True
                }
            return Response(data,status =status.HTTP_200_OK)       
        else:
            data = {
                "message":"Please provide correct credentials",
                "success":False
                }
            return Response(data,status = status.HTTP_400_BAD_REQUEST)




        # user = authenticate(username= username, password=password)
        # if user is not None:
        #     payload = {
        #     "username" : username,
        #     "password" : password
        #     }
        #     encoded_jwt = jwt.encode(payload, key, algorithm="HS256")
        #     print(encoded_jwt)
        #     data = {
        #         "message":"signed in successfuly",
        #         "username":user.username,
        #         "first_name":user.first_name,"last_name":user.last_name,
        #         "token":encoded_jwt,
        #         "success":True
        #         }
        #     return Response(data,status =status.HTTP_200_OK)       
        # else:
        #     data = {
        #         "message":"Please provide correct credentials",
        #         "success":False
        #         }
        #     return Response(data,status = status.HTTP_400_BAD_REQUEST)



from rest_framework.serializers import Serializer
from django.db import IntegrityError

class Signup(APIView):

    def post(self,request):
        name = request.data.get("name")
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        # msg = []
        # try:
            
        #     user = User.objects.create_user(username, email,password)
        #     msg.append("user signed successfully")
        # except IntegrityError as e:
        #     if 'UNIQUE constraint' in str(e.args):
        #         print(str(e.args))
        #         if 'UNIQUE constraint failed: auth_user.username' in (str(e.args)):
        #             error_msg ='usesrname already taken'
        #             msg.append(error_msg)

        #         # elif 'UNIQUE constraint failed: auth_user.email' in (str(e.args)):
        #         #     error_msg ='email already taken'
        #         #     msg.append(error_msg)
                    
        # return Response({"msg": msg})
        users_collection = DB["users"]
        my_input = {"name":name,"userrname":username,"password": password,"email":email}

        find_mine = users_collection.find_one({"username":username,"email":email})
        if find_mine is not None:
            print("already user")  
        else:
            dct = users_collection.insert_one(my_input)
            print("signup successfully")
        return Response({"user":"signedup"})


from utils import AuthAPIView

class PostApiView(AuthAPIView):
    def get(self,request):
        # post = Post.objects.all()
        # Serializer = PostSerializers(post,many = True)
        # return Response(Serializer.data)

        users_collection = DB["users"]
        data = list(users_collection.find({},{"_id":0}))
        return Response(data)


    def post(self,request):
        serializer = PostSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from.models import Like
class LikeApiView (APIView):
    def post(self,request):
        post_id = request.data.get('post_id')
        user_id = request.data.get('user_id')

        is_liked = None

        try:
            like = Like.objects.get(post_id = post_id, user_id = user_id)
            is_liked = True
        except ObjectDoesNotExist:
            is_liked = False 

        msg = ""

        if is_liked == True:
            # unlike the post
            like.delete()
            msg="post like successfuly"
        else:
            #like the post
            msg = "post unliked successfuly"
            like_to_save = Like(post_id = post_id, user_id = user_id)
            like_to_save.save()

        return Response({"message":msg})


class CommentApiView(APIView):
    def get(self,request):
        pass

    def post(self,request):
        user_id = request.data.get('user_id')
        post_id = request.data.get('post_id')
        comment = request.data.get('comment')

        comment = Comment(post_id = post_id, user_id = user_id,comment = comment)
        comment.save()
        msg = ""
        msg = "commented successfuly"

        return Response({"message":msg})
        

    def delete(self,request):
        comment_id = request.data.get("comment_id")
        msg = ""
        try:
            comment = Comment.objects.get(id = comment_id)
            comment.delete()
            msg = "comment deleted"

        except:
            
            msg = " no comment is found"

        return Response({"msg":msg})
