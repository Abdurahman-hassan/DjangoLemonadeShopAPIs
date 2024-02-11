from decimal import Decimal

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from LittlelemonAPI.models import MenuItem, Category


# 1- The first serializer to get all items using a normal serializer
class MenuItemSerializerManual(serializers.Serializer):
    """
    This is a manual serializer to get all the items using the serializer
    """
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=30)

    # # this is a method that we can use to change the representation of the data
    def to_representation(self, instance):
        """
        This method is used to change the representation of the data
        :param instance: the instance of the model
        :return: the representation of the data
        """
        # show all the data
        representation = super().to_representation(instance)
        # print(representation)
        # change the title to only show the first 2 characters
        representation['title'] = representation['title'][:30]
        return representation

    # or we can use the SerializerMethodField
    # title = serializers.SerializerMethodField()
    # def get_title(self, obj):
    #     # Return the first 30 characters of the title
    #     return obj.title[:30]

    # or we can use the method name
    # title = serializers.SerializerMethodField(method_name='get_title')
    # def get_title(self, obj: MenuItem):
    #     return obj.title[:30]

    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()


# def create(self, validated_data):
#     return MenuItem.objects.create(**validated_data)
#
# def update(self, instance, validated_data):
#     instance.title = validated_data.get('title', instance.title)
#     instance.price = validated_data.get('price', instance.price)
#     instance.inventory = validated_data.get('inventory', instance.inventory)
#     instance.save()
#     return instance


# 2- The second serializer to get all items using a model serializer
class CategorySerializer(serializers.ModelSerializer):
    """
    This is a serializer to get all the categories using the model serializer
    """

    class Meta:
        """
        This is the metaclass that we use to define the model and the fields that we want to serialize
        """
        model = Category
        fields = ('id', 'slug', 'title')


# 3- The third serializer to get all items using a model serializer
class MenuItemSerializerAutomatic(serializers.ModelSerializer):
    """
    This is a serializer to get all the items using the model serializer
    """
    # change the name of the field in the serializer
    # it will be stock instead of inventory in the json response
    # {"title": "test_title", "price": "12", "stock": "1", "price_after_tax": 2.0, "category": 1}
    # we should mention the source of the original field "inventory"
    # stock = serializers.IntegerField(source='inventory', min_value=0)
    stock = serializers.IntegerField(source='inventory')
    # add a method to the serializer, add a new field to the serializer
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # add a field from a related model
    # instead of using the id of the category -> 'category' : 1 by default
    # it will be 'category' : 'The first category'

    # this will return the __str__ method of the model
    # we need also use select_related in the view to get the category in the same query,
    # not in a separate query for each menu item
    # we need to add source='category' to get the category field from the related model
    # and show it in the json response
    # we can avoid that by re-name the field to category
    category_str = serializers.StringRelatedField(source='category')
    # category_hyperlink = serializers.HyperlinkedRelatedField(
    #     queryset= Category.objects.all(),
    #     view_name='category-detail',
    #     source='category'
    # )
    # we will use a nested serializer
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    # category = serializers.HyperlinkedRelatedField(
    #     queryset= Category.objects.all(), # this is the queryset that we will use to get the data
    #     view_name='category-detail', # this is the name of the view in urls.py
    #     # we used it if we didn't follow the convention of the view name
    #     # if our view name url was category-detail we don't need to use this
    # )

    # or we can use HyperlinkedModelSerializer instead of ModelSerializer
    # class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    #     class Meta:
    #         model = MenuItem
    #         fields = ('id', 'title', 'price', 'inventory', 'category')
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # title = serializers.CharField(
    #     max_length=255,
    #     validators=[UniqueValidator(queryset=MenuItem.objects.all())])

    class Meta:
        model = MenuItem
        fields = ['id', 'title',
                  'price', 'stock',
                  'price_after_tax',
                  'category_str',
                  # 'category_hyperlink',
                  'category_id',
                  'category']

        # that will make the combination of title and price field unique.
        # With this validation, there will be no duplicate entry of an item with the same price.
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title', 'price']
            ),
        ],

        extra_kwargs = {
            # 'price': {'min_value': 2, 'max_digits': 6, 'decimal_places': 2},
            # 'stock': {'source': 'inventory', 'min_value': 0}
            # To make sure that the title field remains unique in the MenuItems table
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ],
            }
        }

        # instead of using categorySerializer() we can use the depth option
        # all relationships in this serializer will display every field related to that model
        # depth = 1

        # add a new method to the serializer

        def calculate_tax(self, product: MenuItem):
            return product.price * Decimal(1.1)

        # The 2 errors will appear at the same time
        # def validate_price(self, value):
        #     if value is None:
        #         raise serializers.ValidationError('Price cannot be null')
        #     if value < Decimal('2.0'):
        #         raise serializers.ValidationError('Price should not be less than 2.0')
        #     return value
        #
        # def validate_stock(self, value):
        #     if (value < 0):
        #         raise serializers.ValidationError('Stock cannot be negative')
        #     return value

        # or we can use the validate method to validate the data
        # one error will appear and if we fix it, the other error will appear
        def validate(self, attrs):
            if (attrs['price'] < 5):
                raise serializers.ValidationError('Price should not be less than 5.0')
            if (attrs['inventory'] < 0):
                raise serializers.ValidationError('Stock cannot be negative')
            return super().validate(attrs)
