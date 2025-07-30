from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.db import transaction

from .models import Election, Candidate, Vote, UserProfile, AuditLog
from .forms import CustomUserCreationForm, VoteForm, ElectionForm, CandidateForm, UserProfileForm


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_audit(user, action, details, request):
    """Log audit trail"""
    AuditLog.objects.create(
        user=user,
        action=action,
        details=details,
        ip_address=get_client_ip(request)
    )


def home(request):
    """Home page showing active elections"""
    current_time = timezone.now()
    
    # Get active elections
    ongoing_elections = Election.objects.filter(
        is_active=True,
        start_time__lte=current_time,
        end_time__gte=current_time
    )
    
    upcoming_elections = Election.objects.filter(
        is_active=True,
        start_time__gt=current_time
    )
    
    finished_elections = Election.objects.filter(
        end_time__lt=current_time
    ).order_by('-end_time')[:5]  # Last 5 finished elections
    
    context = {
        'ongoing_elections': ongoing_elections,
        'upcoming_elections': upcoming_elections,
        'finished_elections': finished_elections,
    }
    
    return render(request, 'voting_app/home.html', context)


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_audit(user, 'USER_REGISTERED', f'New user registered: {user.username}', request)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the voting system.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'voting_app/register.html', {'form': form})


class ElectionListView(ListView):
    """List all elections"""
    model = Election
    template_name = 'voting_app/election_list.html'
    context_object_name = 'elections'
    paginate_by = 10
    
    def get_queryset(self):
        return Election.objects.filter(is_active=True)


class ElectionDetailView(LoginRequiredMixin, DetailView):
    """Election detail view with voting capability"""
    model = Election
    template_name = 'voting_app/election_detail.html'
    context_object_name = 'election'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        election = self.object
        user = self.request.user
        
        # Check if user has already voted
        user_vote = Vote.objects.filter(voter=user, election=election).first()
        context['user_vote'] = user_vote
        
        # Get candidates with vote counts (only show after election ends or if user is admin)
        candidates = election.candidates.all()
        if election.is_finished or user.is_staff:
            candidates = candidates.annotate(vote_count=Count('votes'))
        
        context['candidates'] = candidates
        context['can_vote'] = election.is_ongoing and not user_vote
        
        # Voting form
        if context['can_vote']:
            context['vote_form'] = VoteForm(election=election, user=user)
        
        return context


@login_required
def cast_vote(request, election_id):
    """Handle vote casting"""
    election = get_object_or_404(Election, id=election_id)
    
    if request.method == 'POST':
        form = VoteForm(election=election, user=request.user, data=request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    vote = form.save(ip_address=get_client_ip(request))
                    log_audit(
                        request.user, 
                        'VOTE_CAST', 
                        f'Vote cast in election: {election.title}', 
                        request
                    )
                    messages.success(request, 'Your vote has been cast successfully!')
                    return redirect('election_detail', pk=election_id)
            except Exception as e:
                messages.error(request, f'Error casting vote: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    
    return redirect('election_detail', pk=election_id)


@login_required
def election_results(request, election_id):
    """View election results"""
    election = get_object_or_404(Election, id=election_id)
    
    # Only show results if election is finished or user is admin
    if not (election.is_finished or request.user.is_staff):
        messages.error(request, 'Results are not yet available for this election.')
        return redirect('election_detail', pk=election_id)
    
    # Get candidates with vote counts and percentages
    candidates = election.candidates.annotate(
        vote_count=Count('votes')
    ).order_by('-vote_count')
    
    total_votes = election.total_votes
    
    # Calculate percentages
    for candidate in candidates:
        candidate.percentage = (candidate.vote_count / total_votes * 100) if total_votes > 0 else 0
    
    context = {
        'election': election,
        'candidates': candidates,
        'total_votes': total_votes,
    }
    
    return render(request, 'voting_app/election_results.html', context)


@login_required
def profile(request):
    """User profile view"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found. Please contact administrator.')
        return redirect('home')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            log_audit(request.user, 'PROFILE_UPDATED', 'User profile updated', request)
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    # Get user's voting history
    votes = Vote.objects.filter(voter=request.user).select_related('election', 'candidate')
    
    context = {
        'form': form,
        'user_profile': user_profile,
        'votes': votes,
    }
    
    return render(request, 'voting_app/profile.html', context)


# Admin views (require staff permissions)

def is_staff(user):
    """Check if user is staff"""
    return user.is_staff


@user_passes_test(is_staff)
def admin_dashboard(request):
    """Admin dashboard"""
    total_elections = Election.objects.count()
    active_elections = Election.objects.filter(is_active=True).count()
    total_users = UserProfile.objects.count()
    total_votes = Vote.objects.count()
    
    # Recent activity
    recent_votes = Vote.objects.select_related('voter', 'candidate', 'election').order_by('-timestamp')[:10]
    recent_registrations = UserProfile.objects.select_related('user').order_by('-created_at')[:10]
    
    context = {
        'total_elections': total_elections,
        'active_elections': active_elections,
        'total_users': total_users,
        'total_votes': total_votes,
        'recent_votes': recent_votes,
        'recent_registrations': recent_registrations,
    }
    
    return render(request, 'voting_app/admin_dashboard.html', context)


@user_passes_test(is_staff)
def admin_elections(request):
    """Admin election management"""
    elections = Election.objects.all().order_by('-created_at')
    paginator = Paginator(elections, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'voting_app/admin_elections.html', {'page_obj': page_obj})


@user_passes_test(is_staff)
def create_election(request):
    """Create new election"""
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            log_audit(request.user, 'ELECTION_CREATED', f'Created election: {election.title}', request)
            messages.success(request, 'Election created successfully!')
            return redirect('admin_elections')
    else:
        form = ElectionForm()
    
    return render(request, 'voting_app/create_election.html', {'form': form})


@user_passes_test(is_staff)
def manage_candidates(request, election_id):
    """Manage candidates for an election"""
    election = get_object_or_404(Election, id=election_id)
    candidates = election.candidates.all()
    
    if request.method == 'POST':
        form = CandidateForm(election=election, data=request.POST, files=request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()
            log_audit(request.user, 'CANDIDATE_ADDED', f'Added candidate: {candidate.name} to {election.title}', request)
            messages.success(request, f'Candidate {candidate.name} added successfully!')
            return redirect('manage_candidates', election_id=election_id)
    else:
        form = CandidateForm(election=election)
    
    context = {
        'election': election,
        'candidates': candidates,
        'form': form,
    }
    
    return render(request, 'voting_app/manage_candidates.html', context)


@user_passes_test(is_staff)
def delete_candidate(request, candidate_id):
    """Delete a candidate"""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    election_id = candidate.election.id
    
    if request.method == 'POST':
        candidate_name = candidate.name
        election_title = candidate.election.title
        candidate.delete()
        log_audit(request.user, 'CANDIDATE_DELETED', f'Deleted candidate: {candidate_name} from {election_title}', request)
        messages.success(request, f'Candidate {candidate_name} deleted successfully!')
    
    return redirect('manage_candidates', election_id=election_id)


# API endpoints for AJAX requests

@login_required
def api_election_status(request, election_id):
    """Get election status via API"""
    election = get_object_or_404(Election, id=election_id)
    
    data = {
        'is_ongoing': election.is_ongoing,
        'is_upcoming': election.is_upcoming,
        'is_finished': election.is_finished,
        'total_votes': election.total_votes,
        'time_left': None,
    }
    
    if election.is_ongoing:
        time_left = election.end_time - timezone.now()
        data['time_left'] = int(time_left.total_seconds())
    
    return JsonResponse(data)
