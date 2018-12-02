from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    return {
        'userId': user.pk,
        'username': user.username,
        'email': user.email,
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token
    }
