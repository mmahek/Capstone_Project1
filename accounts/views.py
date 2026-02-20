from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm, UserForm, ProfileForm


# SIGNUP
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:profile")
    else:
        form = CustomSignupForm()

    return render(request, "registration/signup.html", {"form": form})


# PROFILE PAGE
@login_required
def profile(request):
    profile = request.user.profile
    return render(request, "accounts/profile.html", {"profile": profile})


# EDIT PROFILE
@login_required
def edit_profile(request):

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("accounts:profile")

    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


# LOGOUT
def custom_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("accounts:profile")
