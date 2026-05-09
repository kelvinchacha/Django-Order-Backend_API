"""
Module: users.apps
Description: Configuration for the Users application.
             Handles application metadata and registry.
"""
from django.apps import AppConfig

class UsersConfig(AppConfig):
    """
    Standard Django App configuration for Identity & Access Management.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    # Jina litakalotokea kwenye Django Admin Panel
    verbose_name = 'Usimamizi wa Watumiaji (IAM)'

    def ready(self):
        """
        Hapa ndipo unapoweka 'Signals' (kama unazo) 
        kwa ajili ya kuanzisha mambo fulani app ikishawaka.
        """
        pass