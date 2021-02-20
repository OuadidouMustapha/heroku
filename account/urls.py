from django.urls import path
from .views import SignUpView
from .viewsets import UserList, current_user
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'account'

urlpatterns = [
    path('token-auth/', obtain_jwt_token),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('current_user/', current_user),
    path('users/', UserList.as_view())

]
