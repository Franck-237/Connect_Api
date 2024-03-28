from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoToggleCompleteSerializer
from TodoList.models import Todo
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class TodoList(generics.ListAPIView):
    serializer_class = TodoSerializer
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('created_at')
    
class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
class TodoToggleComplete(generics.UpdateAPIView):
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_update(self, serializer):
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save()

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)

            username = data['username']
            email = data['usermail']
            telephone = data['userphone']
            password1 = data['password1']
            password2 = data['password2']

            if password1 !=  password2:
                return JsonResponse({'error':"Password don't match. Please try again"})
            
            try:
                User.objects.get(username=username)
                return JsonResponse({'error': 'This username have been already taken.'}, status = 400)
            except User.DoesNotExist:
                pass

            try:
                User.objects.get(email=email)
                return JsonResponse({'error': 'This usermail have been already taken.'}, status = 400)
            except User.DoesNotExist:
                pass

            user = User.objects.create_user(
                username = username, 
                email = email,
                phone = telephone,
                password = password1
            )
            user.save()

            token = Token.objects.create(user = user)
            return JsonResponse({'token':str(token)}, status = 201)
        except IntegrityError:
            return JsonResponse({'error':'user name taken. Choose another user name please'}, status = 400)
    return JsonResponse({'error': 'Invalid request method. Use POST for signup.'}, status = 500)

@csrf_exempt
def login(request):
    if  request.method == "POST":
        data = JSONParser().parse(request)

        username = data['username']
        email = data['usermail']
        password = data['password']

        user = authenticate(
            request,
            username = username,
            email = email,
            password = password
        )
        if  user is not None :
            return JsonResponse({'error':'Unable to login. Check username and password.'}, status = 400)
        else :
            try:
                token = Token.objects.get(user = user)
            except:
                token = Token.objects.create(user = user)
            return JsonResponse({'token':str(token)}, status = 201)
    return JsonResponse({'error': 'Invalid request method. Use POST for signup.'}, status = 500)