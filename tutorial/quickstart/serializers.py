from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Product, Category

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'  #cách 1
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at'] #cách 2
        read_only_fields = ['created_at', 'updated_at'] #optional

    def validate_price(self, value):
        """Custom validation"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value
    
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        """Create a new category"""
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update an existing category"""
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance