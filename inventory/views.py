from rest_framework import generics, permissions
from .models import Item
from .serializers import ItemSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
import logging
from rest_framework import viewsets, status
import redis
from django.core.cache import cache
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

redis_client = redis.StrictRedis(host='localhost', port=6380, db=0)

# Set up logger
logger = logging.getLogger(__name__)


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logger.info('List items request received.')
        cached_items = cache.get('items')
        if cached_items:
            logger.info('Returning cached items.')
            return Response(json.loads(cached_items), status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Cache the serialized data for 1 hour
        cache.set('items', json.dumps(serializer.data), timeout=3600)
        logger.info('Items cached for 1 hour.')

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'Retrieve item request received for item ID: {
                    kwargs.get("pk")}.')
        item_id = kwargs.get('pk')
        cached_item = cache.get(f'item_{item_id}')
        if cached_item:
            logger.info('Returning cached item.')
            return Response(json.loads(cached_item), status=status.HTTP_200_OK)

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Cache the serialized individual item for 1 hour
        cache.set(f'item_{item_id}', json.dumps(serializer.data), timeout=3600)
        logger.info('Item cached for 1 hour.')

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        logger.info('Create item request received.')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            self.clear_cache()  # Clear cache after creating an item
            logger.info('Item created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning('Item creation failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        logger.info(f'Update item request received for item ID: {
                    kwargs.get("pk")}.')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            item = serializer.save()
            self.clear_cache()  # Clear cache after updating an item
            logger.info('Item updated successfully.')
            return Response(serializer.data)

        logger.warning('Item update failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'Delete item request received for item ID: {
                    kwargs.get("pk")}.')
        instance = self.get_object()
        instance.delete()
        self.clear_cache()  # Clear cache after deleting an item
        logger.info('Item deleted successfully.')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def clear_cache(self):
        # Clear the cache for items
        cache.delete('items')
        logger.info('Cache cleared for items.')

    def handle_exception(self, exc):
        logger.error(f'Error occurred: {exc}')
        return super().handle_exception(exc)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        logger.info(f'User created: {user.username}')
        return user


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info('User registration request received.')
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            logger.info(f'User registered successfully: {user.username}')
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        logger.warning('User registration failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    logger.info('Home page accessed.')
    return render(request, 'home.html')
