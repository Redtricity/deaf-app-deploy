from django.forms import ModelForm
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import Profile, IdentityTag
from django.forms.widgets import DateInput
from django_countries.widgets import CountrySelectWidget

# -------------------------------------------------------Login--------------------------------------------------------------------------

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-2'),
            Field('password', css_class='mb-2'),
            Submit('submit', 'Log in', css_class='btn btn-primary mt-2')
        )

# --------------------------------------------------Profile------------------------------------------------------------------------------

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    hearing_status = forms.ChoiceField(choices=Profile.HEARING_STATUS_CHOICES, required=False, label="Hearing Status")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")  

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'hearing_status', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='mb-2'),
            Field('email', css_class='mb-2'),
            Field('password1', css_class='mb-2'),
            Field('password2', css_class='mb-2'),
            Field('hearing_status', css_class='mb-2'),
            Field('profile_picture', css_class='mb-2'),  
            Submit('submit', 'Register', css_class='btn btn-primary mt-2 w-100')
        )

    def save(self, commit=True):
        user = super().save(commit)
        hearing_status = self.cleaned_data.get('hearing_status', 'prefer_not_to_say')
        profile_picture = self.cleaned_data.get('profile_picture') 
        Profile.objects.create(
            user=user,
            hearing_status=hearing_status,
            profile_picture=profile_picture  
        )
        return user

        
class ProfileSearchForm(forms.Form):
    search_term = forms.CharField(label='Search', max_length=100)
    
    
class ProfileForm(forms.ModelForm):
    identity_tags = forms.ModelMultipleChoiceField(
        queryset=IdentityTag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Deaf-aware identity tags"
    )

    class Meta:
        model = Profile
        fields = [
            'bio', 'location', 'city', 'birth_date',
            'hearing_status', 'sign_language_preference',
            'identity_tags', 'profile_picture'
        ]
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'location': CountrySelectWidget(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Glasgow or London'}),
        }
