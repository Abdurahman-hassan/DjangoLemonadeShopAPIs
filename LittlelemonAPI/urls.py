from django.urls import path, include

from LittlelemonAPI.views import (
    MenuItemView,
    SingleMenuItemView,
    category_detail,
    menu_items,
    single_item,
    menu_items_basic_fetch_data
)

urlpatterns = [
    # class-based views GenericAPIViews
    path('menu-items', MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(), name='single-menu-item'),

    # function-based views
    path('menu-items-basic', menu_items_basic_fetch_data, name='multi-menu-items-api-view'),
    path('menu-items-basic/<int:pk>', single_item, name='single-menu-item-api-view'),

    path('menu-items-apiview', menu_items, name='menu-items-api-view'),
    # There is a convention you must follow when you create this view name.
    # The rule is that you have to add -detail after the related field name,
    # which is category in the MenuItemSerializer.
    # This is why the view name was category-detail in this code.
    # If the related field name was user, the view name would be user-detail.
    path('category/<int:pk>', category_detail, name='category-detail'),

    path('__debug__/', include('debug_toolbar.urls')),
]
