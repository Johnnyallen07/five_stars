from django.shortcuts import render, get_object_or_404, redirect

from five_stars.models import CustomUser
from .forms import *


def user_profile(request):
    user_id = request.session.get('id')
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Optionally add a success message or redirect
            return redirect('home')
        else:
            return render(request, 'user_profile.html', {'form': form})
    else:
        form = UserForm(instance=user)
        return render(request, 'user_profile.html', {'form': form})
