from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from LittlelemonAPI.models import MenuItem, Category
from LittlelemonAPI.serializers import (MenuItemSerializer, CategorySerializer,
                                        MenuItemSerializerManual,
                                        )


# 1- The first view
# Using generics to create the views
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# 2- The second view
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# 3- The third view
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

# @api_view()
# def single_item(request, pk):
#     menu_item = MenuItem.objects.get(pk=pk)
#     # we didn't use many=True because we are only serializing one object
#     serializer = MenuItemSerializerManual(menu_item)
#     return Response(serializer.data)


@api_view()
def menu_items(request):
    # select_related is used to get the related object in the same query
    # this is used to avoid the N+1 problem
    # instead of doing a query for each menu item to get the category
    # category = Category.objects.get(pk=menu_item.category_id)
    menu_items = MenuItem.objects.select_related('category').all()
    # return Response(menu_items.values())

    # many=True is used when we want to serialize a queryset
    # this is essentially when we convert a list of objects into JSON

    # context is used to pass the request to the serializer
    # this is used to get the full url of the category
    # because we use HyperlinkedRelatedField in the serializer
    # to get the full url of the category
    serializer = MenuItemSerializer(menu_items, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def single_item(request, pk):
    if request.method == 'GET':
        menu_item = get_object_or_404(MenuItem, pk=pk)
        # we didn't use many=True because we are only serializing one object
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
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
