from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image


class UserProfile(models.Model):
    """Extended user profile with voting-specific information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=20, unique=True, help_text="Unique voter identification")
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField()
    is_eligible = models.BooleanField(default=True, help_text="Whether user is eligible to vote")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.voter_id}"
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class Election(models.Model):
    """Model to represent an election"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_elections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        """Validate election dates"""
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Election start time must be before end time.")
    
    @property
    def is_ongoing(self):
        """Check if election is currently ongoing"""
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time
    
    @property
    def is_upcoming(self):
        """Check if election is upcoming"""
        now = timezone.now()
        return self.is_active and self.start_time > now
    
    @property
    def is_finished(self):
        """Check if election has finished"""
        now = timezone.now()
        return self.end_time < now
    
    @property
    def total_votes(self):
        """Get total number of votes cast in this election"""
        return self.votes.count()


class Candidate(models.Model):
    """Model to represent a candidate in an election"""
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, help_text="Candidate biography/manifesto")
    photo = models.ImageField(upload_to='candidate_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['election', 'name']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.election.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if uploaded
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)
    
    @property
    def vote_count(self):
        """Get number of votes for this candidate"""
        return self.votes.count()
    
    @property
    def vote_percentage(self):
        """Get percentage of votes for this candidate"""
        total_votes = self.election.total_votes
        if total_votes == 0:
            return 0
        return round((self.vote_count / total_votes) * 100, 2)


class Vote(models.Model):
    """Model to represent a vote"""
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        unique_together = ['voter', 'election']  # Ensure one vote per user per election
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name} in {self.election.title}"
    
    def clean(self):
        """Validate vote constraints"""
        # Check if candidate belongs to the election
        if self.candidate.election != self.election:
            raise ValidationError("Candidate must belong to the specified election.")
        
        # Check if election is ongoing
        if not self.election.is_ongoing:
            raise ValidationError("Voting is not currently allowed for this election.")
        
        # Check if voter is eligible
        if hasattr(self.voter, 'userprofile') and not self.voter.userprofile.is_eligible:
            raise ValidationError("User is not eligible to vote.")


class AuditLog(models.Model):
    """Model to track important system events for security"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} - {self.timestamp}"
