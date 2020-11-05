from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path,include
from api.views import fav_delete,fav_details,PostsByUser,Favorites,PostList,CategoryList,PostListPublished, CategoryDetails, CategoryPostList, UserViewSet,ProfileViewSet,VacancyList,post_details,published_list
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()
router.register('users',UserViewSet)
router.register('profile',ProfileViewSet)
urlpatterns = [
    path(r'', include(router.urls)),
    path('login/', obtain_jwt_token),
    path('admin/', PostList.as_view()),
    path('admin/<int:post_id>/', post_details),

    path('posts/', PostListPublished.as_view()),
    path('posts/<int:post_id>/', post_details),
    path('fav/', Favorites.as_view()),
    path('fav/<int:author_id>/', fav_details),

    path('profile/<int:user_id>/posts', PostsByUser),
    path('fav/<int:post_id>/<int:author_id>/', fav_delete),

    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetails.as_view()),
    path('categories/<int:pk>/posts/', CategoryPostList.as_view())

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
