from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Create test user accounts for testing TravellerClicks functionality'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating test user accounts...'))
        
        # Create test traveller account
        try:
            if User.objects.filter(email='traveller@test.com').exists():
                self.stdout.write(self.style.WARNING('Traveller test account already exists'))
                traveller = User.objects.get(email='traveller@test.com')
            else:
                traveller = User.objects.create_user(
                    username='traveller_test',
                    email='traveller@test.com',
                    password='Test123!',
                    first_name='John',
                    last_name='Traveller',
                    user_type='traveller',
                    phone_number='+1234567890',
                    location='New York',
                    is_active=True,
                    is_verified=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created traveller account: {traveller.email}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating traveller account: {e}')
            )

        # Create test service provider account
        try:
            if User.objects.filter(email='provider@test.com').exists():
                self.stdout.write(self.style.WARNING('Provider test account already exists'))
                provider = User.objects.get(email='provider@test.com')
            else:
                provider = User.objects.create_user(
                    username='provider_test',
                    email='provider@test.com',
                    password='Test123!',
                    first_name='Maria',
                    last_name='Provider',
                    user_type='service_provider',
                    phone_number='+0987654321',
                    location='Los Angeles',
                    is_active=True,
                    is_verified=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created provider account: {provider.email}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating provider account: {e}')
            )

        # Create admin user for testing
        try:
            if User.objects.filter(email='admin@test.com').exists():
                self.stdout.write(self.style.WARNING('Admin test account already exists'))
                admin = User.objects.get(email='admin@test.com')
            else:
                admin = User.objects.create_superuser(
                    username='admin_test',
                    email='admin@test.com',
                    password='Admin123!',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created admin account: {admin.email}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin account: {e}')
            )

        self.stdout.write(self.style.SUCCESS('\n=== Test Accounts Summary ==='))
        self.stdout.write(self.style.SUCCESS('🧳 TRAVELLER ACCOUNT:'))
        self.stdout.write(f'   Email: traveller@test.com')
        self.stdout.write(f'   Password: Test123!')
        self.stdout.write(f'   Role: Traveller')
        
        self.stdout.write(self.style.SUCCESS('\n🏢 SERVICE PROVIDER ACCOUNT:'))
        self.stdout.write(f'   Email: provider@test.com')
        self.stdout.write(f'   Password: Test123!')
        self.stdout.write(f'   Role: Service Provider')
        
        self.stdout.write(self.style.SUCCESS('\n👑 ADMIN ACCOUNT:'))
        self.stdout.write(f'   Email: admin@test.com')
        self.stdout.write(f'   Password: Admin123!')
        self.stdout.write(f'   Role: Superuser')
        
        self.stdout.write(self.style.SUCCESS('\n✅ All test accounts are ready for testing!'))