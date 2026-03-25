from django.db import models

class DocumentType(models.TextChoices):
    CGV = 'cgv', 'CGV'
    COOKIES = 'cookies', 'Cookies Policy'
    LEGAL_MENTIONS = 'legal_mentions', 'Legal Mentions'
    PRIVACY_POLICY = 'privacy_policy', 'Privacy Policy'