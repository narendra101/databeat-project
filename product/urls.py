from django.urls import path 
from .views import CreateProductView, DeleteProductView, GetAllProductView

urlpatterns = [    
    path('create', CreateProductView.as_view()),
    path('delete/<str:id>', DeleteProductView.as_view()),
    path('get-all', GetAllProductView.as_view()),
]