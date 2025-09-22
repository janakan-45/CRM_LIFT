from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)  # Generate refresh & access tokens
    refresh['role'] = user.role            # Add role info into token payload
    refresh['username'] = user.username    # Add username info into token payload
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
