from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Post, Category, Main,UserProfile
from api.serializers import CategorySerializer, PostSerializer, MainSerializer, UserSerializer,ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from django.contrib.auth.models import User


# Create your views here.
class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated,)


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date')
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated,)


class PostListPublished(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_published=True).order_by('-date')
    serializer_class = PostSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAuthenticated,)


class CategoryPostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        try:
            category = Category.objects.get(id=self.kwargs.get('pk'))
        except Category.DoesNotExist:
            raise Http404
        queryset = category.posts.filter(is_published=True)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer


@api_view(['GET', 'POST'])
def published_list(request):
    if request.method == 'GET':
        # def get_queryset(self):
        posts = Post.objects.filter(is_published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def post_details(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error': serializer.errors})

    elif request.method == 'DELETE':
        post.delete()
        return Response({'deleted': True})


class VacancyList(APIView):
    def get(self, request):
        vacancies = Post.objects.all()
        serializer = MainSerializer(vacancies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Favorites(generics.ListCreateAPIView):
    queryset = Main.objects.all()
    serializer_class = MainSerializer


@api_view(['GET'])
def PostsByUser(request, user_id):
    if request.method == 'GET':
        posts = Post.objects.filter(author_id=user_id)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def fav_details(request,  author_id):
    try:
        post = Main.objects.filter( author_id = author_id)
    except Post.DoesNotExist as e:
        return Response({'error': str(e)})


    if request.method == 'GET':
        serializer = MainSerializer(post, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({'deleted': True})
@api_view(['GET', 'PUT', 'DELETE'])
def fav_delete(request, post_id, author_id):
    try:
        post = Main.objects.filter( author_id = author_id,post_id=post_id)
    except Post.DoesNotExist as e:
        return Response({'error': str(e)})


    if request.method == 'GET':
        serializer = MainSerializer(post, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({'deleted': True})
# @api_view(['POST'])
# def addFav(request, user_id,post_id):
#     if request.method == 'POST':
#         posts = Post.objects.filter(author_id=user_id)
#
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
