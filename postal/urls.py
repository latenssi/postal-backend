from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_jwt import views as jwt_views

from postal.posts.viewsets import PostViewSet
from postal.user.views import CurrentUserView

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api-token-auth/', jwt_views.obtain_jwt_token),
 	url(r'^api-token-refresh/', jwt_views.refresh_jwt_token),
	url(r'^user/$', CurrentUserView.as_view())
]
