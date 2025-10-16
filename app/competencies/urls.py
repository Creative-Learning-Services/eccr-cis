from django.urls import path
from rest_framework.routers import DefaultRouter

from competencies import views

router = DefaultRouter()

app_name = 'competencies'

urlpatterns = [
    path('managed-data/catalogs', views.DomainList.as_view(),
         name='managed-catalog'),
    path('managed-data/catalogs/<str:provider_id>',
         views.DomainSubGraphList.as_view(), name='managed-catalog-data'),
    path('managed-data/catalogs/<str:provider_id>/<str:experience_id>',
         views.GenericNodeEndpoint.as_view(), name='managed-data'),
]
