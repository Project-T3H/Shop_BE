from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ["username", "email", "password"]
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class TicketImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_import
        fields = "__all__"

class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_Import_Detail
        fields = "__all__"
                                
class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Product
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image']          
      
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Detail
        fields = "__all__"

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"

class OrderItemlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders_Item
        fields = "__all__"

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"

class UserRoleSerializer(serializers.ModelSerializer):
     class Meta:
        model = User_role
        fields = "__all__"