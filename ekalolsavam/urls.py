from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("events.urls")),
    path("", include("judges.urls")),
    path("", include("volunteers.urls")),
]
