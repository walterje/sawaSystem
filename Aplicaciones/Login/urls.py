from django.urls import path
from Aplicaciones.Login.views import *
#app_name = 'login'
urlpatterns = [
    # Login
    path('', LoginFormView.as_view(),name='login'),
    #Logout
    path('logout/', LogoutRedirectView.as_view(),name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password')
   

]