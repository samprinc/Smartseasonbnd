import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartseason.settings')
django.setup()

from core.models import User, Field

def run_seed():
    print("Clearing old data...")
    User.objects.filter(username__in=['admin_user', 'agent_user']).delete()
    
    print("Creating Admin...")
    admin = User.objects.create_superuser('admin_user', 'admin@example.com', 'password123', role='admin')
    
    print("Creating Field Agent...")
    agent = User.objects.create_user('agent_user', 'agent@example.com', 'password123', role='agent')
    
    print("Creating Test Fields...")
    Field.objects.create(name='North Sector', crop_type='Maize', planting_date='2026-04-01', assigned_to=agent)
    Field.objects.create(name='South Sector', crop_type='Wheat', planting_date='2026-03-15', assigned_to=agent)

    print("Success! Admin: admin_user / password123 | Agent: agent_user / password123")

if __name__ == '__main__':
    run_seed()