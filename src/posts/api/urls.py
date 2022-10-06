from django.urls import path , include

#from .views import property_list,property_detail
from .views import ( 
#    HomeProperty, 
    PropertysListAV, 
    PropertysDetailAV, 
    BusinessAV, 
    BusinessDetailAV,
    CommentList,
    CommentDetail,
    CommentCreate,
    BusinessVS,
    UserComment,
    PropertysList,
    )
from rest_framework.routers import DefaultRouter

app_name = 'posts'

router = DefaultRouter()
router.register('business',BusinessVS,basename='business')

urlpatterns = [
  #path('',HomeProperty.as_view(),name='home'),
  
  path('propertys/',PropertysListAV.as_view(),name='property'),
  path('propertys/list/',PropertysList.as_view(),name='property-list'),
  path('propertys/<int:pk>/',PropertysDetailAV.as_view(),name='property-detail'),


  #path('list/',property_list,name='list'),
  #path('<int:pk>/',property_detail,name='detail'),

  path('', include(router.urls)),

  #path('business/',BusinessAV.as_view(),name='business'),
  #path('business/<int:pk>/',BusinessDetailAV.as_view(),name='business-detail'),

  #path('comment/',CommentList.as_view(),name='comment-list'),
  path('propertys/<int:pk>/comment-create/',CommentCreate.as_view(),name='comment-create'),
  path('propertys/<int:pk>/comment/',CommentList.as_view(),name='comment-list'),
  path('propertys/comment/<int:pk>/',CommentDetail.as_view(),name='comment-detail'),
  #path('propertys/comments/<str:username>/',UserComment.as_view(),name='user-comment-detail'),
  path('propertys/comments/',UserComment.as_view(),name='user-comment-detail'),
]
