from django.core.exceptions import ValidationError


def generate_avatar_from_initials(user):
    pass


def validate_github_url(value):
    if value and "github.com" not in value:
        raise ValidationError("Ссылка должна вести на github.com")
    return value
