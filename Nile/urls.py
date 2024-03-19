from django.urls import path, re_path, include
from django.views.static import serve

from Nile import views
from django.conf.urls.static import static
from django.conf import settings
from .views import CategoryList, subcategory_detail

app_name = 'Nile'

urlpatterns = [
    path('', views.index, name='index'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/list/', views.orders_list, name='order_list'),
    path('Nile/admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('Nile/admin/order/pdf/<int:order_id>/', views.admin_order_pdf, name='admin_order_pdf'),
    path('item/create/', views.ItemCreate.as_view(), name='item_create'),
    path('item/<int:pk>/update/', views.ItemCreate.as_view(), name='item_update'),
    path('product/<uuid:pk>/detail/', views.ProductDetail, name='item_detail'),
    path('category/<int:pk>/detail/', views.CategoryDetail.as_view(), name='category_detail'),
    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('subcategory_detail/<int:subcategory_id>/', subcategory_detail, name='subcategory_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
