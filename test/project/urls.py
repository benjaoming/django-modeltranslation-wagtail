from django.conf.urls import url
from django.http.response import HttpResponse


urlpatterns = [
    url("/", lambda x: HttpResponse("hej")),
]