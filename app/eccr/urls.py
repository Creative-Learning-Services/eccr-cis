from django.urls import path
from eccr.views import (
    CompetencyDetailView,
    CompetencyListView,
    CreateNodesView,
    CreateRelationshipToExistingView,
    CreateRelationshipView,
    FrameworkDetailView,
    FrameworkListView,
    FrameworkWithCompetenciesView,
    GraphHealthView,
    WorkRoleDetailView,
    WorkRoleListView,
)

urlpatterns = [
    # Framework endpoints
    path("frameworks/", FrameworkListView.as_view(), name="framework-list"),
    path(
        "frameworks/<str:framework_id>/",
        FrameworkDetailView.as_view(),
        name="framework-detail",
    ),
    path(
        "frameworks/<str:framework_id>/competencies/",
        FrameworkWithCompetenciesView.as_view(),
        name="framework-with-competencies",
    ),
    # Competency endpoints
    path("competencies/", CompetencyListView.as_view(), name="competency-list"),
    path(
        "competencies/<str:id>/",
        CompetencyDetailView.as_view(),
        name="competency-detail",
    ),
    # Work role endpoints
    path("workroles/", WorkRoleListView.as_view(), name="workrole-list"),
    path(
        "workroles/<str:work_role_id>/",
        WorkRoleDetailView.as_view(),
        name="workrole-detail",
    ),
    # Graph operation endpoints
    path("nodes/", CreateNodesView.as_view(), name="create-nodes"),
    path(
        "relationships/", CreateRelationshipView.as_view(), name="create-relationship"
    ),
    path(
        "relationships/existing/",
        CreateRelationshipToExistingView.as_view(),
        name="create-relationship-to-existing",
    ),
    # Health check endpoint
    path("health/", GraphHealthView.as_view(), name="graph-health"),
]
