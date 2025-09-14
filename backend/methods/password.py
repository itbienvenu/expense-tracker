import re

def is_strong_password(password):
    # Common weak patterns to avoid
    weak_patterns = [
        '123456', 'password', 'qwerty', 'letmein', 'welcome',
        'admin', 'monkey', 'sunshine', 'password1', 'abc123'
    ]
    
    errors = []
    
    # Check length
    if len(password) < 12:
        errors.append("Password must be at least 12 characters long")
    
    # Check uppercase letters
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check lowercase letters
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check digits
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    # Check special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character (!@#$%^&*(), etc.)")
    
    # Check for weak patterns
    lower_password = password.lower()
    for pattern in weak_patterns:
        if pattern in lower_password:
            errors.append(f"Password contains a common weak pattern: '{pattern}'")
            break
    
    # Check for sequential characters
    if (re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', lower_password) or
        re.search(r'(012|123|234|345|456|567|678|789|890)', lower_password) or
        re.search(r'(qwer|wert|erty|rtyu|tyui|yuio|uiop|asdf|sdfg|dfgh|fghj|ghjk|hjkl|jkl|zxcv|xcvb|cvbn|vbnm)', lower_password)):
        errors.append("Password contains sequential characters that are easy to guess")
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        errors.append("Password contains repeated characters (e.g., aaa, 111)")
    
    # Check if the password is not based on common substitutions
    common_subs = {
        'a': '@', 's': '$', 'i': '!', 'o': '0', 'e': '3',
        'l': '1', 't': '7', 'b': '8', 'g': '9'
    }
    
    # Simple check for leet speak substitutions
    simple_password = lower_password
    for char, sub in common_subs.items():
        simple_password = simple_password.replace(sub, char)
    
    for pattern in weak_patterns:
        if pattern in simple_password:
            errors.append("Password is based on a common pattern with simple character substitutions")
            break
    
    return (len(errors) == 0, errors)

print(is_strong_password("Bienvenu143@"))