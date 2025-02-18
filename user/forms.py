from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from .models import CustomUser,PriestProfile

class CustomUserCreationForm(UserCreationForm):
    identifier = forms.CharField(label="Email or Phone", max_length=100)
    user_type = forms.ChoiceField(choices=[('user', 'User'), ('priest', 'Priest')], label="Register as")
    experience = forms.IntegerField(required=False, label="Experience (in years)")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")
    profile = forms.ImageField(required=False, label="Profile Picture") 
    address = forms.CharField(max_length=60, required=False, label="Address")
    class Meta:
        model = CustomUser
        fields = ('identifier', 'password1', 'password2')

    def clean_identifier(self):
        identifier = self.cleaned_data.get("identifier")
        if "@" in identifier:  # If it contains '@', assume it's an email
            if CustomUser.objects.filter(email=identifier).exists():
                raise forms.ValidationError("A user with this email already exists.")
        else:  # Otherwise, assume it's a phone number
            if CustomUser.objects.filter(phone_number=identifier).exists():
                raise forms.ValidationError("A user with this phone number already exists.")
        return identifier

    def save(self, commit=True):
        identifier = self.cleaned_data["identifier"]
        password = self.cleaned_data["password1"]
        user_type = self.cleaned_data["user_type"]

        user = CustomUser.objects.create_user(username=identifier, password=password)
    
    # Only create a PriestProfile if the user registers as a priest
        if user_type == 'priest':
            # Create the PriestProfile and link it to the user
            PriestProfile.objects.create(
                user=user,
                experience=self.cleaned_data.get("experience"),
                bio=self.cleaned_data.get("bio"),
                profile=self.cleaned_data.get("profile"),  # Ensure the profile picture is saved
                address=self.cleaned_data.get("address"),
            )
        
        return user
    
    
class EmailOrPhoneLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)



class PriestProfileForm(forms.ModelForm):
    class Meta:
        model = PriestProfile
        fields = ['profile', 'bio', 'experience', 'address']

# class EmailOrPhonePasswordResetForm(PasswordResetForm):
#     identifier = forms.CharField(label="Email or Phone", max_length=100)
    
#     def clean_identifier(self):
#         identifier = self.cleaned_data['identifier']
        
#         if "@" in identifier:
#             try:
#                 user = CustomUser.objects.get(email=identifier)
#             except CustomUser.DoesNotExist:
#                 raise forms.ValidationError("No account found with this email.")
#         else:
#             try:
#                 user = CustomUser.objects.get(phone_number=identifier)
#             except CustomUser.DoesNotExist:
#                 raise forms.ValidationError("No account found with this phone number.")
        
#         return identifier
    
#     def get_users(self, identifier):
#         if "@" in identifier:
#             return CustomUser.objects.filter(email=identifier, is_active=True)
#         else:
#             return CustomUser.objects.filter(phone_number=identifier, is_active=True)