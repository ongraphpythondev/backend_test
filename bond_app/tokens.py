import jwt

from django.http import JsonResponse
from django.conf import settings


def auth_only(view_func):
    def wrap(request, *args, **kwargs):
        token = request.headers.get('token','None')

        if token == 'None':
            return JsonResponse({'message':'token not found'},status=400)
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'token expired'},status = 401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message':'invalid token'}, status = 401)
        return view_func(request, *args, **kwargs)

    return wrap

