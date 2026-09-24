"""
create_users_csv.py
EduPro Analysis Project - Synthetic User Data Generator

Generates 3,000 synthetic users with:
- UserID: U00001 to U03000
- UserName: Realistic user names
- Age: Uniform distribution between 15 and 35
- Gender: ~50% Male / ~50% Female
- Email: Realistic email addresses matching names/handles
- Seed: 42 for reproducibility

Saves to data/users.csv
"""

import os
import csv
import random
from typing import Optional, List, Dict
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

FIRST_NAMES_M = [
    'james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'joseph', 'thomas', 'christopher', 
    'charles', 'daniel', 'matthew', 'anthony', 'mark', 'donald', 'steven', 'andrew', 'paul', 'joshua',
    'kenneth', 'kevin', 'brian', 'george', 'timothy', 'ronald', 'edward', 'jason', 'jeffrey', 'ryan',
    'jacob', 'gary', 'nicholas', 'eric', 'jonathan', 'stephen', 'larry', 'justin', 'scott', 'brandon',
    'benjamin', 'samuel', 'raymond', 'gregory', 'frank', 'alexander', 'patrick', 'jack', 'dennis', 'jerry',
    'tyler', 'aaron', 'jose', 'adam', 'nathan', 'henry', 'peter', 'zachary', 'douglas', 'harold'
]

FIRST_NAMES_F = [
    'mary', 'patricia', 'jennifer', 'linda', 'barbara', 'elizabeth', 'susan', 'jessica', 'sarah', 'karen',
    'lisa', 'nancy', 'betty', 'margaret', 'sandra', 'ashley', 'kimberly', 'emily', 'donna', 'michelle',
    'dorothy', 'carol', 'amanda', 'melissa', 'deborah', 'stephanie', 'rebecca', 'sharon', 'laura', 'cynthia',
    'kathleen', 'amy', 'angela', 'shirley', 'anna', 'brenda', 'pamela', 'emma', 'nicole', 'helen',
    'samantha', 'katherine', 'christine', 'debra', 'rachel', 'carolyn', 'janet', 'catherine', 'maria', 'heather',
    'diane', 'ruth', 'julie', 'olivia', 'joyce', 'virginia', 'victoria', 'kelly', 'lauren', 'christina'
]

LAST_NAMES = [
    'smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller', 'davis', 'rodriguez', 'martinez',
    'hernandez', 'lopez', 'gonzalez', 'wilson', 'anderson', 'thomas', 'taylor', 'moore', 'jackson', 'martin',
    'lee', 'perez', 'thompson', 'white', 'harris', 'sanchez', 'clark', 'ramirez', 'lewis', 'robinson',
    'walker', 'young', 'allen', 'king', 'wright', 'scott', 'torres', 'nguyen', 'hill', 'flores',
    'green', 'adams', 'nelson', 'baker', 'hall', 'rivera', 'campbell', 'mitchell', 'carter', 'roberts'
]

EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']


def generate_users(num_users: int = 3000, seed: int = 42) -> List[List]:
    """
    Generate synthetic user records matching specification.
    """
    np.random.seed(seed)
    random.seed(seed)

    rows = []
    for i in range(1, num_users + 1):
        uid = f"U{i:05d}"
        gender = random.choice(['Male', 'Female'])
        age = random.randint(15, 35)

        if gender == 'Male':
            fn = random.choice(FIRST_NAMES_M)
        else:
            fn = random.choice(FIRST_NAMES_F)
        ln = random.choice(LAST_NAMES)

        # Realistic username patterns
        patterns = [
            f"{fn}{ln}",
            f"{ln}{fn}",
            f"{fn}{random.randint(10, 99)}",
            f"{fn[0]}{ln}",
            f"{ln}{fn[0]}",
        ]
        username = random.choice(patterns)

        email_fn = random.choice(FIRST_NAMES_M + FIRST_NAMES_F)
        email_ln = random.choice(LAST_NAMES)
        email_num = random.randint(0, 99)
        domain = random.choice(EMAIL_DOMAINS)
        email_patterns = [
            f"{email_fn}{email_num:02d}@{domain}",
            f"{email_ln}{email_fn}@{domain}",
            f"{email_fn}{email_ln}@{domain}",
            f"{email_fn[0]}{email_ln}@{domain}",
        ]
        email = random.choice(email_patterns)

        rows.append([uid, username, age, gender, email])

    return rows


def save_users_csv(rows: List[List], output_path: str) -> None:
    """Save user rows to CSV."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['UserID', 'UserName', 'Age', 'Gender', 'Email'])
        writer.writerows(rows)
    print(f"Created {len(rows)} users -> {output_path}")


def main(output_path: Optional[str] = None) -> str:
    """Entry point for generating users.csv."""
    if output_path is None:
        output_path = os.path.join(DATA_DIR, "users.csv")
    rows = generate_users(num_users=3000, seed=42)
    save_users_csv(rows, output_path)
    return output_path


if __name__ == "__main__":
    main()
