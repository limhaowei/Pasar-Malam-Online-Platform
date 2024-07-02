
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Vendor, Registration, Review
from .forms import RegistrationForm, ReviewForm

@login_required
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor_profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})





