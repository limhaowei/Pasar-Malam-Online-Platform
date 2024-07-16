import datetime
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator

from .models import Vendor, Market, MarketApplicant, Notification, Rating, Blog
from .forms import (
    CustomUserCreationForm,
    MarketApplicantForm,
    VendorPageForm,
    BlogForm,
    UploadPaymentForm,
)
from .signals import send_notification_on_approval
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


def logout_vendor(request):
    logout(request)
    return redirect("homepage")


# login.html
def login_vendor(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                request.GET["next"] if "next" in request.GET else "homepage"
            )

        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "login.html")


# register.html
def register_user(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect("edit_vendor_page")

        else:
            messages.success(request, "An error has occurred during registration")

    context = {"form": form}
    return render(request, "register.html", context)


# index.html
def homepage(request):
    blog = Blog.objects.last()
    vendors = Vendor.objects.filter(verified=True)[:6]
    context = {
        "vendors": vendors,
        "blog": blog,
    }
    return render(request, "index.html", context)


# vendors.html / vendor_list.html template (included infinite scroll)
def vendors_page(request):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(Vendor.objects.filter(verified=True), 6)
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


# rate vendor function for vendor_list.html template
def rate_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)

    if request.method == "POST":
        rate = (
            int(request.POST.get("rate1", 0))
            + int(request.POST.get("rate2", 0))
            + int(request.POST.get("rate3", 0))
            + int(request.POST.get("rate4", 0))
            + int(request.POST.get("rate5", 0))
        )
        comment = request.POST.get("comment", "")
        rating = Rating.objects.create(vendor=vendor, rating=rate, comment=comment)

    return redirect("homepage")


# detail.html
def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, "vendor_page.html", {"vendor": vendor})


# user_guide.html
def user_guide(request):
    return render(request, "user_guide.html")


# vendor of the week
def blog(request):
    blog = Blog.objects.last()
    context = {
        "blog": blog,
    }
    return render(request, "blog.html", context)


# Vendor-Specific Operations
# apply slot for market
@login_required(login_url="login")
def apply_market_view(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    if request.method == "POST":
        form = MarketApplicantForm(request.POST, request.FILES)
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


# edit vendor page
@login_required(login_url="login")
def edit_vendor_page(request):
    vendor = request.user.vendor
    if request.method == "POST":
        form = VendorPageForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = VendorPageForm(instance=vendor)
    return render(request, "edit_vendor_page.html", {"form": form})


# dashboard for vendor
@login_required(login_url="login")
def vendor_dashboard(request):
    vendor = request.user.vendor
    markets = Market.objects.filter(date__gt=datetime.date.today()).order_by("date")
    approved_markets = MarketApplicant.objects.filter(vendor=vendor, approved=True)
    print(approved_markets)
    context = {
        "vendor": vendor,
        "markets": markets,
        "approved_markets": approved_markets,
    }
    return render(request, "vendor_dashboard.html", context)


# mark notification as read
@login_required(login_url="login")
def mark_notification_as_read(request):
    notification_id = request.POST.get("notification_id")
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return HttpResponse("Notification marked as read")


@login_required(login_url="login")
def upload_payment_page(request, pk):
    market_applicant = MarketApplicant.objects.get(pk=pk)

    if request.method == "POST":
        form = UploadPaymentForm(request.POST, request.FILES, instance=market_applicant)
        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = UploadPaymentForm(instance=market_applicant)

    return render(request, "payment_proof.html", {"form": form})


# Admin-Specific Operations
# view all applicants for a market
@login_required(login_url="login")
@permission_required("is_superuser")
def market_applicants(request, market_id):
    market = get_object_or_404(Market, pk=market_id)
    applicants = MarketApplicant.objects.filter(market=market)
    return render(
        request, "market_applicants.html", {"market": market, "applicants": applicants}
    )


# approve application
@login_required(login_url="login")
@permission_required("is_superuser")
def approve_application(request, pk):
    market_applicant = MarketApplicant.objects.get(pk=pk)
    market_applicant.approved = True
    market_applicant.save()

    # Send notification using signal
    send_notification_on_approval(sender=None, market_applicant=market_applicant)

    return redirect("market_applicants", market_id=market_applicant.market.id)


# manage market includes creating new market
@login_required(login_url="login")
@permission_required("is_superuser")
def manage(request):
    # Auto clean up uncessary market and market applicants data (30 days from today)
    print(datetime.date.today() - datetime.timedelta(days=30))
    past_market = Market.objects.filter(
        date__lt=datetime.date.today() - datetime.timedelta(days=30)
    )
    print(past_market)

    if past_market:
        market_applicants = MarketApplicant.objects.filter(market__in=past_market)
        print(market_applicants)
        market.delete()

    if request.method == "POST":
        date = request.POST.get("date")
        if date:
            market = Market.objects.create(date=date)
            messages.success(request, "New market created successfully!")
            return redirect("manage")
    markets = Market.objects.all().order_by("date")
    # markets = Market.objects.filter(date__gt=datetime.date.today()).order_by("date")
    return render(request, "manage.html", {"markets": markets})


# allocate booth number for approved market applicants
@login_required(login_url="login")
@permission_required("is_superuser")
def allocate_booth(request, pk):
    market_applicant = MarketApplicant.objects.get(pk=pk)
    print(market_applicant)

    if request.method == "POST":
        allocate_booth = request.POST["booth_no"]
        print(allocate_booth)
        market_applicant.booth_no = allocate_booth
        market_applicant.save()
        return redirect("manage")
    else:
        return render(
            request, "allocate_booth.html", {"market_applicant": market_applicant}
        )


# manage vendors
@login_required(login_url="login")
@permission_required("is_superuser")
def manage_vendor(request):
    vendors = Vendor.objects.all()
    return render(request, "manage_vendors.html", {"vendors": vendors})


# verify vendor
@login_required(login_url="login")
@permission_required("is_superuser")
def verify_vendor(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    vendor.verified = True
    vendor.save()
    return redirect("manage_vendor")


# delete vendor
@login_required(login_url="login")
@permission_required("is_superuser")
def delete_vendor(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    vendor.delete()
    return redirect("manage_vendor")


# create blog for vendor of the week
@login_required(login_url="login")
@permission_required("is_superuser")
def create_blog(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.vendor = vendor
            blog.save()
            return redirect("homepage")
    else:
        form = BlogForm()
    return render(request, "weekly_vendor.html", {"form": form})
