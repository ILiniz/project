from django.contrib import admin
from django.urls import path, include
from polls.views import custom_logout, role_redirect, RoleBasedLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', custom_logout, name='logout'),
    path('redirect/', role_redirect, name='role_redirect'),

    path('', RoleBasedLoginView.as_view(), name='login'),
    path('', include('polls.urls')),
]
