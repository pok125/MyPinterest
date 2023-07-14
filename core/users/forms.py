from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

# settings에 있는 AUTH_USER_MODEL로 명시한 User사용
User = get_user_model()

class JoinForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'username']

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['email', 'password']