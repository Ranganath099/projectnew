from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout,get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm, EmailOrPhoneLoginForm, PriestProfileForm 
from .models import PriestProfile

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in.")
            login(request, user, backend="user.backends.EmailOrPhoneBackend")
            return redirect("user:login")  
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})

User = get_user_model()  # Ensure we use the custom user model

def user_login(request):
    if request.method == "POST":
        form = EmailOrPhoneLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]

            # Try to authenticate the user
            user = authenticate(request, username=identifier, password=password)  

            if user is not None:
                login(request, user)
                if hasattr(user, 'priest_profiles') and user.priest_profiles.exists():
                    # Redirect to the priest dashboard
                    return redirect("/user/dashboard/")
                else:
                    # Redirect to the regular user home page
                    
                # if user.is_superuser:
                #     # Login superuser with both backends
                #     # login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                #     login(request, user)
                # else:
                #     # Login regular users with custom backend
                #     login(request, user, backend="user.backends.EmailOrPhoneBackend")

                    return redirect("/user/home/")  # Redirect all users to home page
            else:
                form.add_error(None, "Invalid email/phone number or password")
    else:
        form = EmailOrPhoneLoginForm()
    
    return render(request, "user/login.html", {"form": form})

@login_required(login_url="/user/login")
def user_home(request):
    return render(request, "user/home.html")


@login_required(login_url="/user/login")
def priest_dashboard(request):
    # Only priests should be able to access this view
    if not hasattr(request.user, 'priest_profiles') or not request.user.priest_profiles.exists():
        return redirect("/user/home/") # If user is not a priest, redirect them to the normal home

    # Render the priest-specific dashboard page
    return render(request, "user/dashboard.html")




# @login_required
def priest_profile(request):
    # Get the priest profile for the logged-in user
    profile, created = PriestProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PriestProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user:dashboard')  # Redirect to dashboard after saving
    else:
        form = PriestProfileForm(instance=profile)
    
    return render(request, 'user/priest_profile.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("user:login")
