#!/usr/bin/env python
"""
Script to create sample elections and candidates for the voting system
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_voting_system.settings')
django.setup()

from voting_app.models import Election, Candidate
from django.contrib.auth.models import User

def create_sample_data():
    """Create sample elections and candidates"""
    
    # Get or create admin user for elections
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: {admin_user.username}")
    else:
        print(f"ℹ️  Using existing admin user: {admin_user.username}")
    
    # Create sample elections
    elections_data = [
        {
            'title': 'Student Council President Election 2025',
            'description': 'Annual election for Student Council President. Choose the leader who will represent student interests and drive positive change on campus.',
            'start_time': timezone.now() - timedelta(hours=2),
            'end_time': timezone.now() + timedelta(days=7),
            'is_active': True,
            'candidates': [
                {'name': 'Alice Johnson', 'bio': 'Computer Science major with 3 years of student government experience. Passionate about technology innovation and student rights.'},
                {'name': 'Bob Smith', 'bio': 'Business Administration student and current Vice President. Focused on improving campus facilities and student services.'},
                {'name': 'Carol Wilson', 'bio': 'Environmental Science major advocating for sustainable campus initiatives and green energy solutions.'}
            ]
        },
        {
            'title': 'Best Programming Language 2025',
            'description': 'Community poll to determine the most popular and effective programming language for modern development projects.',
            'start_time': timezone.now() - timedelta(days=1),
            'end_time': timezone.now() + timedelta(days=14),
            'is_active': True,
            'candidates': [
                {'name': 'Python', 'bio': 'Versatile, readable, and powerful language perfect for AI, web development, and data science applications.'},
                {'name': 'JavaScript', 'bio': 'Essential for web development with growing backend capabilities through Node.js and modern frameworks.'},
                {'name': 'Java', 'bio': 'Enterprise-grade language with strong performance, security features, and extensive ecosystem support.'},
                {'name': 'TypeScript', 'bio': 'JavaScript with static typing, offering better code quality and developer experience for large applications.'}
            ]
        },
        {
            'title': 'Community Center Activities Vote',
            'description': 'Help decide which new activities and programs should be added to our community center this year.',
            'start_time': timezone.now() + timedelta(days=3),
            'end_time': timezone.now() + timedelta(days=10),
            'is_active': True,
            'candidates': [
                {'name': 'Yoga & Meditation Classes', 'bio': 'Weekly wellness sessions promoting mental health and physical fitness for all age groups.'},
                {'name': 'Tech Workshops', 'bio': 'Hands-on workshops covering coding, digital literacy, and emerging technology trends.'},
                {'name': 'Art & Craft Studios', 'bio': 'Creative spaces for painting, pottery, and various artistic endeavors with expert instruction.'}
            ]
        },
        {
            'title': 'Employee of the Month - December 2024',
            'description': 'Vote for the employee who demonstrated exceptional performance, teamwork, and dedication.',
            'start_time': timezone.now() - timedelta(days=30),
            'end_time': timezone.now() - timedelta(days=1),
            'is_active': False,
            'candidates': [
                {'name': 'Sarah Davis', 'bio': 'Marketing specialist who led the successful Q4 campaign, increasing engagement by 40%.'},
                {'name': 'Mike Rodriguez', 'bio': 'Software engineer who optimized system performance and mentored junior developers.'},
                {'name': 'Lisa Chen', 'bio': 'Customer service representative with 98% satisfaction rating and innovative problem-solving.'}
            ]
        }
    ]
    
    print("Creating sample elections and candidates...")
    
    for election_data in elections_data:
        # Create or get election
        election, created = Election.objects.get_or_create(
            title=election_data['title'],
            defaults={
                'description': election_data['description'],
                'start_time': election_data['start_time'],
                'end_time': election_data['end_time'],
                'is_active': election_data['is_active'],
                'created_by': admin_user
            }
        )
        
        if created:
            print(f"✅ Created election: {election.title}")
            
            # Create candidates for this election
            for candidate_data in election_data['candidates']:
                candidate, candidate_created = Candidate.objects.get_or_create(
                    name=candidate_data['name'],
                    election=election,
                    defaults={
                        'bio': candidate_data['bio']
                    }
                )
                
                if candidate_created:
                    print(f"  ➕ Added candidate: {candidate.name}")
                else:
                    print(f"  ⚠️  Candidate already exists: {candidate.name}")
        else:
            print(f"⚠️  Election already exists: {election.title}")
    
    # Print summary
    total_elections = Election.objects.count()
    total_candidates = Candidate.objects.count()
    active_elections = Election.objects.filter(is_active=True).count()
    
    print(f"\n📊 Database Summary:")
    print(f"   Total Elections: {total_elections}")
    print(f"   Active Elections: {active_elections}")
    print(f"   Total Candidates: {total_candidates}")
    print(f"\n🎉 Sample data creation completed successfully!")
    print(f"🌐 Visit http://127.0.0.1:8000/ to see your voting system in action!")

if __name__ == '__main__':
    create_sample_data()
