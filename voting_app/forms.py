from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import UserProfile, Vote, Candidate, Election


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form with voter-specific fields"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    voter_id = forms.CharField(
        max_length=20, 
        required=True,
        help_text="Enter your unique voter ID"
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False,
        help_text="Optional: Your phone number"
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="You must be 18 or older to register"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_voter_id(self):
        """Validate voter ID uniqueness"""
        voter_id = self.cleaned_data['voter_id']
        if UserProfile.objects.filter(voter_id=voter_id).exists():
            raise ValidationError("This voter ID is already registered.")
        return voter_id

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_date_of_birth(self):
        """Validate age requirement (18+)"""
        date_of_birth = self.cleaned_data['date_of_birth']
        today = timezone.now().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        
        if age < 18:
            raise ValidationError("You must be at least 18 years old to register.")
        
        if date_of_birth > today:
            raise ValidationError("Date of birth cannot be in the future.")
        
        return date_of_birth

    def save(self, commit=True):
        """Save user and create associated UserProfile"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                voter_id=self.cleaned_data['voter_id'],
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth']
            )
        return user


class VoteForm(forms.Form):
    """Form for casting votes in an election"""
    candidate = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None,
        required=True
    )

    def __init__(self, election, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.election = election
        self.user = user
        self.fields['candidate'].queryset = election.candidates.all()
        self.fields['candidate'].label = "Select your candidate:"

    def clean_candidate(self):
        """Validate voting constraints"""
        candidate = self.cleaned_data['candidate']
        
        # Check if user has already voted in this election
        if Vote.objects.filter(voter=self.user, election=self.election).exists():
            raise ValidationError("You have already voted in this election.")
        
        # Check if election is ongoing
        if not self.election.is_ongoing:
            raise ValidationError("Voting is not currently open for this election.")
        
        # Check if user is eligible to vote
        if hasattr(self.user, 'userprofile') and not self.user.userprofile.is_eligible:
            raise ValidationError("You are not eligible to vote.")
        
        return candidate

    def save(self, ip_address=None):
        """Save the vote"""
        candidate = self.cleaned_data['candidate']
        vote = Vote.objects.create(
            voter=self.user,
            candidate=candidate,
            election=self.election,
            ip_address=ip_address
        )
        return vote


class ElectionForm(forms.ModelForm):
    """Form for creating/editing elections (admin use)"""
    
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_time', 'end_time', 'is_active']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        """Validate election timing"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("Election start time must be before end time.")
            
            # Don't allow past start times for new elections
            if not self.instance.pk and start_time < timezone.now():
                raise ValidationError("Election start time cannot be in the past.")
        
        return cleaned_data


class CandidateForm(forms.ModelForm):
    """Form for adding/editing candidates"""
    
    class Meta:
        model = Candidate
        fields = ['name', 'party', 'bio', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, election=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.election = election

    def clean_name(self):
        """Validate candidate name uniqueness within election"""
        name = self.cleaned_data['name']
        if self.election:
            existing_candidate = Candidate.objects.filter(
                election=self.election, 
                name=name
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_candidate.exists():
                raise ValidationError(f"A candidate named '{name}' already exists in this election.")
        
        return name


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        """Save both User and UserProfile"""
        profile = super().save(commit=False)
        
        if commit:
            # Update User fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            
            # Save profile
            profile.save()
        
        return profile
