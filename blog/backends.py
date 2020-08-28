from .models import User


class CustomBackend(object):
    def authenticate(self, request, **credentials):
        username = credentials.get('username', credentials.get('username'))
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    
