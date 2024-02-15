from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from LittlelemonAPI.views import (
    MenuItemView,
    SingleMenuItemView,
    category_detail,
    menu_items,
    menu_items_save_to_modelDserializer,
    menu_items_basic_fetch_data, single_item_basic_fetch_data, menu_OpenAPIRenderer,
    menu_TemplateHTMLFormRendererRenderer, menu_StaticHTMLRenderer, menu_CSVRenderer, menu_YAMLRenderer,
    menu_items_filter_data, MenuItemModelView, secret_request
)

urlpatterns = [
    # class-based views GenericAPIViews
    path('menu-items', MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(), name='single-menu-item'),

    # function-based views
    path('menu-items-basic', menu_items_basic_fetch_data, name='multi-menu-items-api-view'),
    path('menu-items-basic/<int:pk>', single_item_basic_fetch_data, name='single-menu-item-api-view'),

    path('menu-items-apiview', menu_items, name='menu-items-api-view'),
    # There is a convention you must follow when you create this view name.
    # The rule is that you have to add -detail after the related field name,
    # which is category in the MenuItemSerializer.
    # This is why the view name was category-detail in this code.
    # If the related field name was user, the view name would be user-detail.
    path('category/<int:pk>', category_detail, name='category-detail'),

    path('menu-items-save', menu_items_save_to_modelDserializer, name='menu-items-save'),
    path('menu-items-save/<int:pk>', menu_items_save_to_modelDserializer, name='menu-items-save'),

    path('menu-OpenAPIRenderer', menu_OpenAPIRenderer, name='menu-items-api-view'),
    path('menu-templateHtmlFormRenderer', menu_TemplateHTMLFormRendererRenderer, name='menu-items-api-view'),
    path('menu-StaticHTMLRenderer', menu_StaticHTMLRenderer, name='menu-items-api-view'),
    path('menu_YAMLRenderer', menu_YAMLRenderer, name='menu-items-api-view'),
    path('menu_CSVRenderer', menu_CSVRenderer, name='menu-items-api-view'),
    path('menu_items_filter_data', menu_items_filter_data, name='menu_items_filter_data'),

    path('menu-items-model-viewset', MenuItemModelView.as_view({'get': 'list'}), name='menu-items-model-viewset'),
    path('menu-items-model-viewset/<int:pk>', MenuItemModelView.as_view({'get': 'retrieve'}), name='menu-items-model-viewset'),
    path('secret_request', secret_request, name='secret_request'),

    # this is provided by the rest_framework drf in-order-to get the token
    # when we hit post-request to this url we will get the token
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('__debug__/', include('debug_toolbar.urls')),
]
