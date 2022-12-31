from django.contrib import admin
from django.urls import path, include
from register.views import PingView, LandingView



urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('admin/', admin.site.urls),
    path('part1/', include('register.urls')),
    path('part2/', include('product.urls')),
    path('ping', PingView.as_view())
]
