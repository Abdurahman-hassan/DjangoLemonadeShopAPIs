from decimal import Decimal

from rest_framework import serializers

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


class MenuItemSerializerAutomatic(serializers.ModelSerializer):
    """
    This is a serializer to get all the items using the model serializer
    """
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
