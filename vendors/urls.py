from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    # path("register/", views.register_vendor, name="register_vendor"),
    path("register/", views.register_user, name="register_user"),
    path("login/", views.login_vendor, name="login"),
    path("logout/", views.logout_vendor, name="logout"),
    path("vendors/", views.vendors_page, name="vendor_list"),
    path("search/", views.search, name="search"),
    path("vendor/<pk>/", views.vendor_detail, name="vendor_detail"),
    path("user-guide/", views.user_guide, name="user_guide"),
    path("blog/", views.blog, name="blog"),
    path("manage/", views.manage, name="manage"),
    path(
        "apply-to-market/<int:market_id>/", views.apply_market_view, name="apply_market"
    ),
    path(
        "market_applicants/<int:market_id>/",
        views.market_applicants,
        name="market_applicants",
    ),
    path(
        "approve_application/<pk>/",
        views.approve_application,
        name="approve_application",
    ),
    path("dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("edit-vendor-page/", views.edit_vendor_page, name="edit_vendor_page"),
    path(
        "mark_notification_as_read/",
        views.mark_notification_as_read,
        name="mark_notification_as_read",
    ),
    path(
        "upload_payment/<pk>/",
        views.upload_payment_page,
        name="upload_payment",
    ),
]
