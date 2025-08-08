from django.urls import path
from .views import bag_list, bag_delete, bag_detail, bag_create, bag_update

urlpatterns = [
    path('bags/', bag_list, name='bag_list'),
    path('bag/<int:pk>/detail', bag_detail, name='bag_detail'),
    path('bag/create/', bag_create, name='bag_create'),
    path('bag/<int:pk>/update', bag_update, name='bag_update'),
    path('bag/<int:pk>/delete', bag_delete, name='bag_delete'),
]

# from .views import ListCreateApiView, DeleteDetailUpdateApiView
#
# urlpatterns = [
#     path('bags/', ListCreateApiView.as_view(), name='bag_list'),
#     path('a/<int:pk>/', DeleteDetailUpdateApiView.as_view(), name='bag_a')
# ]

# from .views import ListCreateApiView, DetailDeleteUpdateApiView
#
# urlpatterns = [
#     path('bags/', ListCreateApiView.as_view(), name='bag-list-create'),
#     path('bags/<int:pk>/', DetailDeleteUpdateApiView.as_view(), name='bag-detail-update-delete'),
# ]



# from django.urls import path
# from .views import ListCreateApiView, DetailDeleteUpdateApiPKView
#
# urlpatterns = [
#     path('bags/', ListCreateApiView.as_view(), name='bag-list-create'),
#     path('bags/<int:pk>/', DetailDeleteUpdateApiPKView.as_view(), name='bag-detail-update-delete'),
# ]

