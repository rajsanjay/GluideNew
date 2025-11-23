"""
Custom social account adapter for Django Allauth.

This adapter customizes the user creation process for social authentication
(e.g., Google OAuth) by automatically assigning new users to the STUDENT group.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social account authentication.

    Extends DefaultSocialAccountAdapter to add custom behavior when saving
    users who sign up via social authentication providers (Google OAuth).
    """

    def save_user(self, request, sociallogin, form=None):
        """
        Save a new user from social authentication.

        Args:
            request: HTTP request object
            sociallogin: Social login instance
            form: Optional form data

        Returns:
            User: The created/updated user instance with STUDENT group assigned
        """
        user = super().save_user(request, sociallogin, form)

        # Assign default group (STUDENT) to new social auth users
        student_group, _ = Group.objects.get_or_create(name='STUDENT')
        user.groups.add(student_group)

        return user
