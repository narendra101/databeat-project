from django.template.response import TemplateResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from .serializers import UserSerializer
from .models import UserModel
from django.views import View
from databeat.settings import SALT

def authenticate(req):
    if req.headers.get('Authorization'):
        token = req.headers.get('Authorization').split(' ')[1]        
    else:
        return False, None        
    payload = jwt.decode(token, SALT, algorithms=["HS256"])
    username = payload.get('name')        
    user = UserModel.objects.filter(name=username).last()
    if user:
        return user.logged_in, user
    else:
        False, None
    

class PingView(View):
    def get(self, *args, **kwargs):
        print(args, kwargs)
        return HttpResponse('pong')


class LandingView(View):
    template = 'index.html'
    def get(self, *args, **kwargs):
        print(args, kwargs)
        return TemplateResponse(self.request, self.template)

class RegisterView(APIView):
    def post(self, *args, **kwargs):
        if self.request.data.get('password') != self.request.data.get('confirm_password'):
            return Response({
                'status': 'failed',
                'reason': 'passwords don\'t match',
                'data': self.request.data,                
            }, status.HTTP_400_BAD_REQUEST)        
        serializer = UserSerializer(data=self.request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status.HTTP_201_CREATED)
        else:
            errors = {}            
            for error in serializer.errors:                
                errors[error] = serializer.errors.get(error)
                for i in range(len(errors[error])):
                    errors[error][i] = errors[error][i].replace(' model', '')
                    
            return Response({'status': 'failed', 'errors': errors}, status.HTTP_400_BAD_REQUEST)

        
class LoginView(APIView):
    def post(self, *args, **kwargs):
        username = self.request.data.get('name')
        password = self.request.data.get('password')        
        user = UserModel.objects.filter(name=username).last()
        if not user:
            return Response({
                'status': 'failed',
                'reason': 'User doesn\'t exist'
            }, status.HTTP_400_BAD_REQUEST)        
        if user.password != password:
            return Response({
                'status': 'failed',
                'reason': 'Incorrect password'
            }, status.HTTP_400_BAD_REQUEST)
        payload = {
            'name': username,
            'password': password
        }        
        token = jwt.encode(payload, SALT, algorithm='HS256')
        user.logged_in = True
        user.jwt_token = token
        user.save()
        return Response({
            'status': 'success',
            'message': 'User logged in Successfully',
            'token': token
        }, status.HTTP_200_OK)

class LogoutView(APIView):
    def get(self, *args, **kwargs):        
        logged_in, user = authenticate(self.request)        
        if logged_in:
            user.logged_in = False
            user.save()
            return Response({
                'status': 'success',
                'message': 'Logged out successfully'
            }, status.HTTP_200_OK)            
        return Response({
            'status': 'failed',
            'message': 'User is not logged in'
        }, status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    def get(self, *args, **kwargs):
        logged_in, user = authenticate(self.request)
        if logged_in:
            return Response({
                'status': 'success',
                'message': 'Authenticated user!!'
            }, status.HTTP_200_OK)            
        else:
            return Response({
                'status': 'Failed',
                'message': 'Authentication Failure'
            }, status.HTTP_400_BAD_REQUEST)            






