from django.contrib import admin
from django.urls import path,include
from .views import homeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homeView.as_view(),name='home'),
    path('store/',include('posts.api.urls',namespace='posts')),
    path('account/',include('user_app.api.urls',namespace='user-app')),
    #path('api-auth/',include('rest_framework.urls')),
]
