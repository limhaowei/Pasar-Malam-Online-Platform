from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator

from .models import Vendor, Market, MarketApplicant, Notification
from .forms import VendorForm, MarketApplicantForm, VendorPageForm
from .signals import send_notification_on_approval
from django.contrib.auth import logout


def logout_vendor(request):
    logout(request)
    return redirect("homepage")


# register-vendor.html / register_vendor.html template
def register_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = VendorForm()
    return render(request, "register_vendor.html", {"form": form})


# login.html
def login_vendor(request):
    return render(request, "login.html")


# index.html
def homepage(request):
    selected_vendor = Vendor.objects.all().first()
    vendors = Vendor.objects.all()[:6]
    context = {
        "vendors": vendors,
        "selected_vendor": selected_vendor,
        "blog_title": "Vendor of the Week",
        "blog_content": "This is the content of the blog",
    }
    return render(request, "index.html", context)


# vendors.html / vendor_list.html template (included infinite scroll)
def vendors_page(request):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(Vendor.objects.all(), 6)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    return render(request, "vendor_list.html", context)


# search function for vendor_list.html template
def search(request):
    search = request.GET.get("q")
    page_number = request.GET.get("page", 1)

    if search:
        vendors = Vendor.objects.filter(name__icontains=search)
    else:
        vendors = Vendor.objects.none()

    paginator = Paginator(vendors, 6)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    return render(request, "vendor_list.html", context)


# detail.html
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, "vendor_page.html", {"vendor": vendor})


# user_guide.html
def user_guide(request):
    return render(request, "user_guide.html")


# # apply_slot.html
# def apply_slot(request):
#     context = {
#         "month": "July",
#         "year": "2024",
#     }
#     return render(request, "apply_slot.html", context)


# vendor of the week
def blog(request):
    selected_vendor = Vendor.objects.all().first()
    context = {
        "selected_vendor": selected_vendor,
        "title": "Vendor of the Week",
        "content": "This is the content of the blog",
    }
    return render(request, "blog.html", context)


# admin actions
@login_required(login_url="login")
def apply_market_view(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    if request.method == "POST":
        form = MarketApplicantForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.vendor = request.user.vendor
            application.market = market
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect("vendor_dashboard")
    else:
        form = MarketApplicantForm()
    return render(request, "apply_market.html", {"form": form, "market": market})


@login_required(login_url="login")
@permission_required("is_superuser")
def manage(request):
    if request.method == "POST":
        date = request.POST.get("date")
        if date:
            market = Market.objects.create(date=date)
            messages.success(request, "New market created successfully!")
            return redirect("manage")
    markets = Market.objects.all()
    return render(request, "manage.html", {"markets": markets})


@login_required(login_url="login")
@permission_required("is_superuser")
def market_applicants(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    applicants = MarketApplicant.objects.filter(market=market)
    return render(
        request, "market_applicants.html", {"market": market, "applicants": applicants}
    )


@login_required(login_url="login")
@permission_required("is_superuser")
def approve_application(request, pk):
    market_applicant = MarketApplicant.objects.get(pk=pk)
    market_applicant.approved = True
    market_applicant.save()

    # Send notification using signal
    send_notification_on_approval(sender=None, market_applicant=market_applicant)

    return redirect("market_applicants_list")


@login_required(login_url="login")
def edit_vendor_page(request):
    vendor = request.user.vendor
    if request.method == "POST":
        form = VendorPageForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = VendorPageForm(instance=vendor)
    return render(request, "edit_vendor_page.html", {"form": form})


@login_required(login_url="login")
def vendor_dashboard(request):
    vendor = request.user.vendor
    return render(request, "vendor_dashboard.html", {"vendor": vendor})


@login_required(login_url="login")
def mark_notification_as_read(request):
    notification_id = request.POST.get("notification_id")
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return HttpResponse("Notification marked as read")
