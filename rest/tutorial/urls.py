from django.urls import path, re_path

from .views import EchoView, FiboView

urlpatterns = [
    re_path(r'^tutorial/?$', EchoView.as_view()),
    re_path(r'^fibonacci/?$', FiboView.as_view()),
    re_path(r'^logs/?$', FiboView.as_view())
]
