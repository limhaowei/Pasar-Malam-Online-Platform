
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vendor
from .forms import VendorForm




def register_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = VendorForm()
    return render(request, 'register_vendor.html', {'form': form})


def homepage(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})


def vendor_page(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, 'vendor_page.html', {'vendor': vendor})



