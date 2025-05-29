from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create a user
username = "testuser"
password = "TestPassword123!"

try:
    # Check if user already exists
    user = User.objects.get(username=username)
    print(f"User {username} already exists.")
except User.DoesNotExist:
    # Create new user
    user = User.objects.create_user(
        username=username, password=password, email="testuser@example.com"
    )
    print(f"Created user {username}.")

# Generate JWT token
try:
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    print("\nJWT Tokens:")
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
except Exception as e:
    print(f"Error generating JWT token: {e}")

