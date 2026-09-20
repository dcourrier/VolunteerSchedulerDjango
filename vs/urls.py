from django.urls import include, path
#from debug_toolbar.toolbar import debug_toolbar_urls
from . import views

app_name = "vs"
urlpatterns = [
    path("", views.initial, name="initial"),
    path("dash", views.dashboard_view, name="dashboard"),
    path("vs/assignments", views.DummyView.as_view(), name="assignments"),
    path("vs/events", views.DummyView.as_view(), name="events"),
    path("vs/forgotPassword", views.DummyView.as_view(), name="forgotPassword"),
    path("vs/home/", views.Home.as_view(), name="home"),
    path("vs/households", views.DummyView.as_view(), name="households"),
    path("vs/login/", views.LoginView.as_view(), name="tryLogin"),
    path("vs/logout/", views.logout, name="tryLogout"),
    path("vs/locations", views.DummyView.as_view(), name="locations"),
    path("vs/organizations", views.DummyView.as_view(), name="organizations"),
    path("vs/passwordChange", views.DummyView.as_view(), name="passwordChange"),
    path("vs/resources", views.DummyView.as_view(), name="resources"),
    path("vs/reports", views.DummyView.as_view(), name="reports"),
    path("vs/schedules", views.DummyView.as_view(), name="schedules"),
    path("vs/selectOrg", views.DummyView.as_view(), name="selectOrg"),
    path("vs/skills", views.DummyView.as_view(), name="skills"),
    path("vs/utilities", views.DummyView.as_view(), name="utilities"),
    path("vs/volunteerHome", views.DummyView.as_view(), name="volunteerHome"),
    path("vs/volunteerAvailability", views.DummyView.as_view(), name="volunteerAvailability"),
    path("vs/volunteerEventPreferences", views.DummyView.as_view(), name="volunteerEventPreferences"),
    path("vs/volunteerJobAssignments", views.DummyView.as_view(), name="volunteerJobAssignments"),
    path("vs/volunteerRelationships", views.DummyView.as_view(), name="volunteerRelationships"),
    path("vs/volunteers", views.DummyView.as_view(), name="volunteers"),
] #+ debug_toolbar_urls()