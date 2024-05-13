from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=username, password=password)

        if user is not None:
            # Authentication successful
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def account(request):
    user = request.user
    account = Account.objects.get(id=user.id)
    
    if request.method == "GET":        
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)
    elif request.method == "DELETE":
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def accountCreate(request):
    if request.method == "POST":
        serializer = AccountSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def form(request):
    if request.method == "GET":
        user = request.user
        forms = Form.objects.filter(creator = user)
        serializer = FormSerializer(forms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])       
def aform(request, pk):
    user = request.user
    form = Form.objects.get(id=pk, creator=user)
    if request.method == "DELETE":
        form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "GET":
        serializer = FormSerializer(form, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def formpreview(request, pk):
    form = Form.objects.get(id=pk)
    if request.method == "GET":
        serializer = FormSerializer(form, many=False)
        return Response(serializer.data)
    
@api_view(['GET'])
def formcomponents(request, pk):
    form = Form.objects.get(id=pk)
    comps = FormComponent.objects.filter(form=form).order_by('order')
    if request.method == "GET":
        serializer = FormCompSerializer(comps, many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET']) 
@permission_classes([IsAuthenticated])  
def componentcreate(request):
    comps = FormComponent.objects.all()
    if request.method == "POST":
        serializer = FormCompSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":
        serializer = FormCompSerializer(comps, many=True)
        return Response(serializer.data)


