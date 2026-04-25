import secrets
import string

def generate_short_id(length: int = 3) -> str:
    """Generates a random short ID string."""
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
