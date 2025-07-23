from django.urls import path
from .views import RequestCodeView, VerifyCodeView, ProfileAPIView, UseInviteView

urlpatterns = [
    path('auth/request_code/', RequestCodeView.as_view(), name='request-code'),
    path('auth/verify_code/', VerifyCodeView.as_view(), name='verify-code'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/use_invite/', UseInviteView.as_view(), name='use-invite'),
]
