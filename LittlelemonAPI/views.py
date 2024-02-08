from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from LittlelemonAPI.models import MenuItem, Category
from LittlelemonAPI.serializers import (CategorySerializer,
                                        MenuItemSerializerManual, MenuItemSerializerAutomatic,
                                        )


# 1- The first view to get all items
# Using generics to create, List data
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializerAutomatic


# 2- The second view to get a single item
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializerAutomatic


# 3- The third view to get all items
@api_view()
def menu_items_basic_fetch_data(request):
    # using a model directly
    # menu_items = MenuItem.objects.all()
    # return Response(menu_items.values())

    # using a serializer
    items = MenuItem.objects.all()
    # many=True is used when we want to serialize a queryset
    # this is essentially when we convert a list of objects into JSON
    serializer_item = MenuItemSerializerManual(items, many=True)
    return Response(serializer_item.data)


# 4- The fourth view to get a single item
@api_view()
def single_item_basic_fetch_data(request, pk):
    # menu_item = MenuItem.objects.get(pk=pk)
    # we use get_object_or_404 to return a 404 response if the object is not found instead of raising an exception
    menu_item = get_object_or_404(MenuItem, pk=pk)
    # we didn't use many=True because we are only serializing one object not a queryset
    serializer = MenuItemSerializerManual(menu_item)
    return Response(serializer.data)


@api_view()
def menu_items(request):
    # select_related is used to get the related object in the same query
    # this is used to avoid the N+1 problem
    # instead of doing a query for each menu item to get the category of the menu item
    # category = Category.objects.get(pk=menu_item.category_id)
    # we can get the category in the same query
    menu_items = MenuItem.objects.select_related('category').all()
    # return Response(menu_items.values())

    # many=True is used when we want to serialize a queryset
    # this is essentially when we convert a list of objects into JSON

    # context is used to pass the request to the serializer
    # this is used to get the full url of the category
    # because we use HyperlinkedRelatedField in the serializer
    # to get the full url of the category
    serializer = MenuItemSerializerAutomatic(menu_items, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def single_item(request, pk):
    if request.method == 'GET':
        menu_item = get_object_or_404(MenuItem, pk=pk)
        # we didn't use many=True because we are only serializing one object
        serializer = MenuItemSerializerAutomatic(menu_item)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MenuItemSerializerAutomatic(data=request.data)
        # we can use raise_exception=True to raise an exception if the serializer is not valid
        # instead of using if serializer.is_valid()
        # and return a response with status 400 if the serializer is not valid
        serializer.is_valid(raise_exception=True)
        # call the validated date through the serializer
        # serializer.validated_data # this will return a dictionary of the validated data
        # or we can use serializer.save() to save the data
        serializer.save()
        # we can't access the data if the data is not saved
        return Response(serializer.data, status=HTTP_201_CREATED)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)
