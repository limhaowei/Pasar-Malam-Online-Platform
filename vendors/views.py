from django.shortcuts import render, redirect, get_object_or_404

from .models import Vendor
from .forms import VendorForm
from django.core.paginator import Paginator


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
def login(request):
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


# apply_slot.html
def apply_slot(request):
    context = {
        "month": "July",
        "year": "2024",
    }
    return render(request, "apply_slot.html", context)


# vendor of the week
def blog(request, pk):
    selected_vendor = Vendor.objects.all().first()
    context = {
        "selected_vendor": selected_vendor,
        "title": "Vendor of the Week",
        "content": "This is the content of the blog",
    }
    return render(request, "blog.html", context)
