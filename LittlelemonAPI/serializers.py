from decimal import Decimal

from rest_framework import serializers

from LittlelemonAPI.models import MenuItem, Category


class MenuItemSerializerManual(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=2)

    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # inventory = serializers.IntegerField()


# def create(self, validated_data):
#     return MenuItem.objects.create(**validated_data)
#
# def update(self, instance, validated_data):
#     instance.title = validated_data.get('title', instance.title)
#     instance.price = validated_data.get('price', instance.price)
#     instance.inventory = validated_data.get('inventory', instance.inventory)
#     instance.save()
#     return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'title')


class MenuItemSerializer(serializers.ModelSerializer):
    # change the name of the field we should add it into fields
    stock = serializers.IntegerField(source='inventory')
    # add a method to the serializer
    price_after_tax = serializers.SerializerMethodField(method_name='claculate_tax')
    # add a field from a related model
    # instead of using the id of the category -> 'category' : 1 by default
    # it will be 'category' : 'title'
    # category = serializers.StringRelatedField()

    # we will use a nested serializer
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    # category = serializers.HyperlinkedRelatedField(
    #     queryset= Category.objects.all(), # this is the queryset that we will use to get the data
    #     view_name='category-detail', # this is the name of the view in urls.py
    #     # we used it if we didn't follow the convention of the view name
    #     # if our view name url was category-detail we don't need to use this
    # )

    class Meta:
        model = MenuItem
        fields = ['id', 'title',
                  'price', 'stock',
                  'price_after_tax', 'category', 'category_id']
        # instead of using categorySerializer() we can use the depth option
        # all relationships in this serializer will display every field related to that model
        # depth = 1

    # add a new method to the serializer
    def claculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)

# or we can use HyperlinkedModelSerializer
# class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ('id', 'title', 'price', 'inventory', 'category')
