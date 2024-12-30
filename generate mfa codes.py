import pyotp
import time
from collections import defaultdict
from typing import Dict, List, Tuple
 
def generate_and_analyze_codes(secret: str, count: int = 1000000) -> Tuple[List[str], Dict[int, int]]:
    """
    Generate MFA codes and analyze their digit counts
    
    Args:
        secret: The secret key for TOTP generation
        count: Number of codes to generate (default 1000)
        
    Returns:
        Tuple containing:
        - List of generated codes
        - Dictionary mapping digits (0-9) to their total count across all codes
    """
    # Initialize TOTP generator
    totp = pyotp.TOTP(secret)
    
    # Get current timestamp
    current_time = int(time.time())
    
    # Generate codes
    codes = []
    digit_counts = defaultdict(int)
    
    for i in range(count):
        # Generate code for current timestamp + 30s intervals
        timestamp = current_time + (i * 30)  # TOTP standard interval is 30 seconds
        code = totp.at(timestamp)
        codes.append(code)
        
        # Count digits in this code
        for digit in code:
            digit_counts[int(digit)] += 1
    
    return codes, dict(digit_counts)
 
def analyze_code_patterns(codes: List[str]) -> Dict[str, int]:
    """
    Analyze patterns in the generated codes
    
    Args:
        codes: List of generated MFA codes
        
    Returns:
        Dictionary containing various pattern statistics
    """
    patterns = {
        'total_codes': len(codes),
        'unique_codes': len(set(codes)),
        'codes_with_repeating_digits': sum(1 for code in codes if any(code.count(d) > 1 for d in code)),
        'codes_starting_with_zero': sum(1 for code in codes if code.startswith('0')),
    }
    
    return patterns
 
def main():
    # Generate a random secret key (in practice, this would be provided by the service)
    secret = pyotp.random_base32()
    print(f"Using secret key: {secret}")
    
    # Generate codes and analyze
    codes, digit_counts = generate_and_analyze_codes(secret)
    patterns = analyze_code_patterns(codes)
    
    # Print results
    print("\nDigit frequency analysis:")
    for digit, count in sorted(digit_counts.items()):
        print(f"Digit {digit}: {count} occurrences")
    
    print("\nPattern analysis:")
    for pattern, value in patterns.items():
        print(f"{pattern}: {value}")
    
    # Print first few codes as example
    print("\nFirst 5 generated codes:")
    for i, code in enumerate(codes[:5]):
        print(f"Code {i+1}: {code}")
    
    return codes, digit_counts, patterns
 
if __name__ == "__main__":
    codes, digit_counts, patterns = main()
