from django.shortcuts import render
from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from .email_utils import send_verification_email, send_welcome_email

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Optimized registration with built-in Django features"""
    serializer = UserRegistrationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid data provided',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():  # Ensure data consistency
            # Use Django's built-in create_user method for better security
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', ''),
                phone_number=serializer.validated_data.get('phone_number', ''),
                location=serializer.validated_data.get('location', ''),
                is_verified=False
            )
            
            # Generate verification token
            user.generate_verification_token()
            user.save(update_fields=['verification_token', 'verification_token_expires'])
            
            # Send verification email asynchronously would be better for performance
            email_sent = send_verification_email(user)
            
            if email_sent:
                return Response({
                    'message': 'Registration successful! Please check your email for a verification link.',
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'Registration successful but failed to send verification email. Please contact support.',
                    'email': user.email,
                    'requires_resend': True
                }, status=status.HTTP_201_CREATED)
                
    except ValidationError as e:
        return Response({
            'error': 'Validation error',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Registration failed. Please try again.',
            'details': str(e) if settings.DEBUG else None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Optimized login with caching and built-in Django authentication"""
    serializer = UserLoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    # Use Django's built-in authenticate for security
    user = authenticate(username=email, password=password)
    
    if not user:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check verification status
    if not user.is_verified:
        return Response({
            'error': 'Please verify your email address before logging in.',
            'requires_verification': True,
            'email': user.email,
            'can_resend': True
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Use get_or_create for token efficiency 
    token, created = Token.objects.get_or_create(user=user)
    
    # Cache user data for better performance (optional)
    cache_key = f"user_data_{user.id}"
    cached_user_data = cache.get(cache_key)
    
    if not cached_user_data:
        cached_user_data = UserSerializer(user).data
        cache.set(cache_key, cached_user_data, 300)  # Cache for 5 minutes
    
    return Response({
        'token': token.key,
        'user': cached_user_data
    }, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_view(request):
    """Optimized email verification with better error handling"""
    token = request.data.get('token')
    
    if not token:
        return Response({
            'error': 'Verification token is required.',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Debug logging
    print(f"DEBUG: Received verification token: {token}")
    
    try:
        # First, let's see if any user has this token (regardless of verification status)
        users_with_token = User.objects.filter(verification_token=token)
        print(f"DEBUG: Found {users_with_token.count()} users with this token")
        
        if users_with_token.exists():
            for user in users_with_token:
                print(f"DEBUG: User {user.email} - is_verified: {user.is_verified}, token_expires: {user.verification_token_expires}")
        
        # Use select_for_update for concurrency safety
        with transaction.atomic():
            user = User.objects.select_for_update().get(
                verification_token=token,
                is_verified=False  # Only get unverified users
            )
            
            print(f"DEBUG: Found unverified user: {user.email}")
            
            # Check if token is valid and not expired
            if user.is_verification_token_valid(token):
                print(f"DEBUG: Token is valid for user {user.email}")
                # Verify the user atomically
                user.is_verified = True
                user.verification_token = None  # Clear the token
                user.verification_token_expires = None
                user.save(update_fields=['is_verified', 'verification_token', 'verification_token_expires'])
                
                # Clear any cached user data
                cache_key = f"user_data_{user.id}"
                cache.delete(cache_key)
                
                # Send welcome email (could be made async for better performance)
                send_welcome_email(user)
                
                return Response({
                    'message': 'Email verified successfully! You can now log in to your account.',
                    'success': True,
                    'can_login': True
                }, status=status.HTTP_200_OK)
            else:
                print(f"DEBUG: Token is invalid or expired for user {user.email}")
                print(f"DEBUG: Token expiry: {user.verification_token_expires}, Current time: {timezone.now()}")
                return Response({
                    'error': 'Verification token is invalid or has expired. Please request a new verification email.',
                    'success': False,
                    'can_resend': True
                }, status=status.HTTP_400_BAD_REQUEST)
                
    except User.DoesNotExist:
        print(f"DEBUG: No unverified user found with token: {token}")
        return Response({
            'error': 'Invalid verification token or account already verified.',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"DEBUG: Exception during verification: {str(e)}")
        return Response({
            'error': 'Verification failed. Please try again.',
            'success': False,
            'details': str(e) if settings.DEBUG else None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_view(request):
    """Optimized resend verification with rate limiting consideration"""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email address is required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check rate limiting (basic implementation)
        rate_limit_key = f"resend_verification_{email}"
        if cache.get(rate_limit_key):
            return Response({
                'error': 'Please wait before requesting another verification email.',
                'can_retry_after': 60  # seconds
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        user = User.objects.get(email=email)
        
        if user.is_verified:
            return Response({
                'message': 'This email address is already verified.',
                'already_verified': True
            }, status=status.HTTP_200_OK)
        
        # Generate new verification token
        user.generate_verification_token()
        user.save(update_fields=['verification_token', 'verification_token_expires'])
        
        # Send new verification email
        email_sent = send_verification_email(user)
        
        if email_sent:
            # Set rate limit (1 minute)
            cache.set(rate_limit_key, True, 60)
            
            return Response({
                'message': 'New verification email sent successfully. Please check your inbox.',
                'email_sent': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Failed to send verification email. Please try again later.',
                'email_sent': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except User.DoesNotExist:
        # Don't reveal if email exists for security
        return Response({
            'message': 'If an account with this email exists, a verification email has been sent.',
            'email_sent': True  # Always return true for security
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Failed to process request. Please try again later.',
            'details': str(e) if settings.DEBUG else None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# For backward compatibility
RegisterView = register_view
LoginView = login_view
ProfileView = profile_view
VerifyEmailView = verify_email_view
ResendVerificationView = resend_verification_view