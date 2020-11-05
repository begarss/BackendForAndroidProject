from .serializers import UserSerializer,ProfileSerializer #you have already created UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    user = UserSerializer(user, context={'request': request}).data
    # profile = ProfileSerializer(userprofile, context={'request': request}).data

    return {
        'token': token,
        'userid': user['id'],
        'username':user['username'],
        'is_superuser':user['is_superuser'],
        'profile':user['profile_pic']
    }