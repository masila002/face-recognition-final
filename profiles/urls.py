from django.urls import path
from . import views, views_scan


urlpatterns = [
    path("index/", views.login_view, name="index"),  # Root URL mapped to home view
    # path("students/", views.employees, name="students"),
    path("home/", views.home_view, name="home"),
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("classify/", views.find_user_view, name="classify"),
    path("profile/", views.user_profile, name="profile"),
    path("employees/", views.employees, name="employees"),
    # Newly added links
    path("face_login/", views.face_login, name="face_login"),
    path("upload_face_login/", views.upload_face_login, name="upload_face_login"),
    path("password_login/", views.user_login, name="password_login"),
    path("register/", views.register, name="register"),
    ## for the views_scan file implementing user login and logout status
    path(
        "face_scan/", views_scan.face_scan, name="face_scan"
    ),  # Endpoint for face recognition (login/logout)
    path(
        "attendance_records/", views_scan.attendance_records, name="attendance_records"
    ),  # View for attendance records
    path("process_frame/", views.process_frame, name="process_frame"),
]
