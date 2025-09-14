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

def password_strength_meter(password):
    if not password:
        return (0, ["Password cannot be empty"])
    
    score = 0
    suggestions = []
    
    # Length contributes up to 25 points
    length_score = min(25, len(password) * 2)
    score += length_score
    
    # Character variety contributes up to 50 points
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    variety_count = sum([has_upper, has_lower, has_digit, has_special])
    variety_score = variety_count * 12.5  # 12.5 points per variety type
    score += variety_score
    
    # Simple check for mixed case and special characters
    if has_upper and has_lower:
        score += 5
    if has_special:
        score += 10
    if len(password) > 16:
        score += 10
    
    # Penalties for weak patterns
    weak_patterns_penalty = 0
    lower_password = password.lower()
    weak_terms = ['password', '123', 'qwerty', 'admin', 'letmein', 'welcome']
    
    for term in weak_terms:
        if term in lower_password:
            weak_patterns_penalty += 20
    
    score = max(0, score - weak_patterns_penalty)
    
    # Generate suggestions
    if len(password) < 12:
        suggestions.append("Use at least 12 characters")
    if not has_upper:
        suggestions.append("Add uppercase letters")
    if not has_lower:
        suggestions.append("Add lowercase letters")
    if not has_digit:
        suggestions.append("Add numbers")
    if not has_special:
        suggestions.append("Add special characters (!@#$% etc.)")
    if weak_patterns_penalty > 0:
        suggestions.append("Avoid common words and patterns")
    
    return (min(100, score), suggestions)