from rest_framework.serializers import ModelSerializer
from .models import Product, Survey, DiscountItem


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class DiscountItemSerializer(ModelSerializer):
    class Meta:
        model = DiscountItem
        fields = '__all__'
