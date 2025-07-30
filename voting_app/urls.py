# cspell:ignore uidb64
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='voting_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Election views
    path('elections/', views.ElectionListView.as_view(), name='election_list'),
    path('elections/<int:pk>/', views.ElectionDetailView.as_view(), name='election_detail'),
    path('elections/<int:election_id>/vote/', views.cast_vote, name='cast_vote'),
    path('elections/<int:election_id>/results/', views.election_results, name='election_results'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    
    # Admin views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/elections/', views.admin_elections, name='admin_elections'),
    path('admin/elections/create/', views.create_election, name='create_election'),
    path('admin/elections/<int:election_id>/candidates/', views.manage_candidates, name='manage_candidates'),
    path('admin/candidates/<int:candidate_id>/delete/', views.delete_candidate, name='delete_candidate'),
    
    # API endpoints
    path('api/elections/<int:election_id>/status/', views.api_election_status, name='api_election_status'),
    
    # Password reset views
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='voting_app/password_reset.html',
             email_template_name='voting_app/password_reset_email.html',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='voting_app/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='voting_app/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='voting_app/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
