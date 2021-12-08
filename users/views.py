from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    # send for validation if POST
    if request.method == 'POST':
        # django form
        form = UserRegisterForm(request.POST)
        # check validation
        if form.is_valid():
            # secure the password with hash
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! you are now able to log in {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


@login_required # decorator for checking if user is login
def profile(request):
    if request.method == 'POST':
        # for see the current details of user- instance=request.user
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated Successfully!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
            'u_form': u_form,
            'p_form': p_form
        }

    return render(request, 'users/profile.html', context)
