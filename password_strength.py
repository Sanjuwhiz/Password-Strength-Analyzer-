import re
import random
import string
import hashlib
import datetime
import os

print("=== Ultimate Password Security Analyzer ===")
print("1. Check Password")
print("2. Generate Strong Password")

choice = input("Choose option (1/2): ")

COMMON_WORDS = ["admin", "welcome", "login", "password"]
KEYBOARD_PATTERNS = ["qwerty", "asdf", "12345"]

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def password_used_before(pwd):
    if not os.path.exists("password_history.txt"):
        return False
    with open("password_history.txt") as f:
        return hash_password(pwd) in f.read()

def save_password_history(pwd):
    with open("password_history.txt", "a") as f:
        f.write(hash_password(pwd) + "\n")

def check_password(password):
    strength = 0
    issues = []

    if len(password) >= 8:
        strength += 1
    else:
        issues.append("Password too short")

    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        issues.append("No uppercase letter")

    if re.search(r"[a-z]", password):
        strength += 1
    else:
        issues.append("No lowercase letter")

    if re.search(r"[0-9]", password):
        strength += 1
    else:
        issues.append("No number")

    if re.search(r"[!@#$%^&*]", password):
        strength += 1
    else:
        issues.append("No special character")

    for word in COMMON_WORDS:
        if word in password.lower():
            issues.append("Contains common dictionary word")

    for pattern in KEYBOARD_PATTERNS:
        if pattern in password.lower():
            issues.append("Keyboard pattern detected")

    if re.search(r"(.)\1{2,}", password):
        issues.append("Repeated characters detected")

    if password_used_before(password):
        issues.append("Password reused previously")

    score_percent = int((strength / 5) * 100)

    level = "STRONG" if strength == 5 else "MEDIUM" if strength >= 3 else "WEAK"

    print("\nSecurity Score:", score_percent, "%")
    print("Strength Level:", level)
    print("Change Reminder: Every 90 days recommended")

    if issues:
        print("\nSecurity Issues Found:")
        for issue in issues:
            print("-", issue)

    save_password_history(password)

    with open("password_report.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {level} | {score_percent}%\n")

    with open("password_summary.txt", "w") as f:
        f.write("Password Analysis Completed Successfully\n")

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choice(chars) for _ in range(14))
    print("\nGenerated Secure Password:", pwd)

if choice == "1":
    pwd = input("Enter password: ")
    check_password(pwd)
elif choice == "2":
    generate_password()
else:
    print("Invalid option")
