from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import UserProfile, Election, Candidate, Vote, AuditLog


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('voter_id', 'phone_number', 'date_of_birth', 'is_eligible')


# Extended User admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_voter_id', 'get_is_eligible', 'is_active')
    list_filter = UserAdmin.list_filter + ('userprofile__is_eligible',)
    
    def get_voter_id(self, obj):
        try:
            return obj.userprofile.voter_id
        except UserProfile.DoesNotExist:
            return "No Profile"
    get_voter_id.short_description = 'Voter ID'
    
    def get_is_eligible(self, obj):
        try:
            return obj.userprofile.is_eligible
        except UserProfile.DoesNotExist:
            return False
    get_is_eligible.short_description = 'Eligible'
    get_is_eligible.boolean = True


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'voter_id', 'phone_number', 'age', 'is_eligible', 'created_at')
    list_filter = ('is_eligible', 'created_at')
    search_fields = ('user__username', 'user__email', 'voter_id', 'phone_number')
    readonly_fields = ('created_at', 'age')
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Age'


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_active', 'get_status', 'get_total_votes', 'created_by')
    list_filter = ('is_active', 'start_time', 'end_time', 'created_by')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'get_total_votes', 'get_status')
    filter_horizontal = ()
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'created_by')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time', 'is_active')
        }),
        ('Statistics', {
            'fields': ('get_total_votes', 'get_status', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status(self, obj):
        if obj.is_ongoing:
            return format_html('<span style="color: green;">Ongoing</span>')
        elif obj.is_upcoming:
            return format_html('<span style="color: orange;">Upcoming</span>')
        elif obj.is_finished:
            return format_html('<span style="color: red;">Finished</span>')
        else:
            return format_html('<span style="color: gray;">Inactive</span>')
    get_status.short_description = 'Status'
    
    def get_total_votes(self, obj):
        return obj.total_votes
    get_total_votes.short_description = 'Total Votes'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'election', 'get_vote_count', 'get_vote_percentage', 'created_at')
    list_filter = ('election', 'party', 'created_at')
    search_fields = ('name', 'party', 'election__title')
    readonly_fields = ('created_at', 'get_vote_count', 'get_vote_percentage', 'get_photo_preview')
    
    fieldsets = (
        (None, {
            'fields': ('election', 'name', 'party')
        }),
        ('Details', {
            'fields': ('bio', 'photo', 'get_photo_preview')
        }),
        ('Statistics', {
            'fields': ('get_vote_count', 'get_vote_percentage', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_vote_count(self, obj):
        return obj.vote_count
    get_vote_count.short_description = 'Votes'
    
    def get_vote_percentage(self, obj):
        return f"{obj.vote_percentage}%"
    get_vote_percentage.short_description = 'Vote %'
    
    def get_photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="150" height="150" />')
        return "No photo"
    get_photo_preview.short_description = 'Photo Preview'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'candidate', 'election', 'timestamp', 'ip_address')
    list_filter = ('election', 'timestamp', 'candidate__party')
    search_fields = ('voter__username', 'candidate__name', 'election__title')
    readonly_fields = ('voter', 'candidate', 'election', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False  # Prevent adding votes through admin
    
    def has_change_permission(self, request, obj=None):
        return False  # Prevent changing votes through admin


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'details')
    readonly_fields = ('user', 'action', 'details', 'ip_address', 'timestamp')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Customize admin site
admin.site.site_header = "Online Voting System Administration"
admin.site.site_title = "Voting Admin"
admin.site.index_title = "Welcome to Online Voting System Administration"
