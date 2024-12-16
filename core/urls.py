from core.views import HomeView, LogoutViewCustom
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from payments.views import PaymentList, RequestAntecipation

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("payments/", PaymentList.as_view(), name="payment-list"),
    path(
        "request-antecipation/",
        RequestAntecipation.as_view(),
        name="request-antecipation",
    ),
    path("admin/", admin.site.urls),
    path("logout/", LogoutViewCustom.as_view(), name="logout"),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
