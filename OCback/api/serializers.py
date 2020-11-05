from itertools import islice

from rest_framework import serializers
from api.models import Post, Category, Main, UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    catName = serializers.CharField()

    def create(self, validated_data):
        category = Category.objects.create(catName=validated_data.get('catName'))
        return category

    def update(self, instance, validated_data):
        instance.catName = validated_data.get('catName', instance.catName)
        instance.save()
        return instance



class ProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField()

    class Meta:
        model = UserProfile
        fields = ['id','profile_pic','user']
        extra_kwargs = {'user': {'required': False}}
    def update(self, instance, validated_data):
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # userprofile = ProfileSerializer(read_only=True)

    profile_pic = serializers.ImageField(read_only=True,source='userprofile.profile_pic')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_superuser','profile_pic')
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'is_superuser': {'read_only': True, 'required': False}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Token.objects.create(user=user)
        return user


    # def to_representation(self, instance):
    #     data = super(UserSerializer, self).to_representation(instance)
    #     userprofile = data.pop('userprofile')
    #
    #     for key, val in islice(userprofile.items(),1,None):
    #         data.update({key: val})
    #     return data





class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    date = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField()
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        post = Post.objects.create(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            category_id=validated_data.get('category_id'),
            date=validated_data.get('date'),
            author_id=validated_data.get('author_id')
        )
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.date = validated_data.get('data', instance.date)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = UserProfile
#         fields = ('id','user','profile_pic')
#         extra_kwargs = {'user': {'read_only': True, 'required': True}}

class MainSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.IntegerField()
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField()

    class Meta:
        model = Main
        fields = ('id', 'post', 'author', 'post_id', 'author_id','is_favorite')
