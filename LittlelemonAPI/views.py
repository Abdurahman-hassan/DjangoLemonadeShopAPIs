from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, OpenAPIRenderer, JSONOpenAPIRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer

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
def menu_items_save_to_modelDserializer(request, pk=None):
    if request.method == 'GET':
        if pk:
            menu_item = get_object_or_404(MenuItem, pk=pk)
            # we didn't use many=True because we are only serializing one object
            serializer = MenuItemSerializerAutomatic(menu_item)
            return Response(serializer.data)
        else:
            menu_items = MenuItem.objects.all()
            # many=True is used when we want to serialize a queryset
            # this is essentially when we convert a list of objects into JSON
            serializer = MenuItemSerializerAutomatic(menu_items, many=True)
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
        # we can access the data after saving it
        validated_data = serializer.validated_data  # this will return a dictionary of the validated data
        # # we can access the data after saving it
        print(validated_data)
        return Response(serializer.data, status=HTTP_201_CREATED)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)


@api_view()
@renderer_classes([OpenAPIRenderer])
def menu_OpenAPIRenderer(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializerAutomatic(items, many=True)
    return Response({'data': serialized_item.data}, template_name='menu-items.html')


@api_view()
@renderer_classes([JSONOpenAPIRenderer])
def menu_JsonOpenAPIRenderer(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializerAutomatic(items, many=True)
    return Response({'data': serialized_item.data}, template_name='menu-items.html')


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu_TemplateHTMLFormRendererRenderer(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializerAutomatic(items, many=True)
    return Response(data={'data': serialized_item.data}, template_name='menu-items.html')


@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def menu_StaticHTMLRenderer(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)


@api_view(['GET'])
@renderer_classes([CSVRenderer])
def menu_CSVRenderer(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializerAutomatic(items, many=True)
    return Response(serialized_item.data)


@api_view(['GET'])
@renderer_classes([YAMLRenderer])
def menu_YAMLRenderer(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializerAutomatic(items, many=True)
    return Response(serialized_item.data)


# instead of attacging the renderer to the view
# we add it into the settings.py
# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',  # this is used to render the browsable api
#         'rest_framework_xml.renderers.XMLRenderer',  # this is used to render the browsable api
#         'rest_framework_csv.renderers.CSVRenderer',
#         'rest_framework_yaml.renderers.YAMLRenderer',
#     ]
# }

# Now the client can send the following Accept headers to receive the API output in their desired format.


@api_view(['GET', 'POST'])
def menu_items_filter_data(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        # category_name = request.GET.get('category')
        # we can use query_params instead of get
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        # to_price = request.GET.get('to_price')
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            # This is a case-insensitive search that matches any part of the title
            # title is a field in the MenuItem model
            items = items.filter(title__contains=search)
        if ordering:
            # http://127.0.0.1:8000/api/menu_items_filter_data?ordering=-price
            # this will order the items by price in descending order
            # items = items.order_by(ordering)
            # http://127.0.0.1:8000/api/menu_items_filter_data?ordering=-price,inventory
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)  # or in one line items = items.order_by(*ordering.split(','))

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializerAutomatic(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializerAutomatic(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data, status=HTTP_201_CREATED)


class MenuItemModelView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializerAutomatic
    # we can use the filter_backends to filter the data
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['category', 'price']
    ordering_fields = ['price', 'inventory']
    ordering = ['price']  # default ordering
    search_fields = ['title', 'category__title']
    # pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination
    # pagination_class = Cursor


@api_view()
@permission_classes([IsAuthenticated])
def secret_request(request):
    return Response({'message': 'This is a secret message'})


@api_view()
@permission_classes([IsAuthenticated])
def manger_request(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Only the manager can see this message'})
    else:
        return Response({'message': 'You are not a manager'}, status=403)
