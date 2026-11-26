from django.urls import path
from .views import CourseViewSet

# course_list = CourseViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# course_detail = CourseViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# urlpatterns = [
#     path('courses/', course_list, name ="course_list"),
# path('courses/<int:pk>/', course_detail, name= "course_detail"),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import StudentViewSet, CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

