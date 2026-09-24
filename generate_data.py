"""
generate_data.py
EduPro Analysis Project - Synthetic Course & Transaction Data Generator

Generates:
1. Courses dataset (50 realistic courses across 8 categories, 2 types, 3 levels)
   Saved to data/courses.csv
2. Transactions dataset (5,000 - 8,000 transactions between 2023-01-01 and 2024-12-31)
   - Realistic user activity distribution (younger users more active)
   - Realistic course popularity (beginners and free/technology courses more popular)
   - Multi-course enrollments without duplicate course purchases per user
   Saved to data/transactions.csv

Uses seed 42 for reproducibility.
"""

import os
import sys
import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np


# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
COURSES_CSV = os.path.join(DATA_DIR, "courses.csv")
TRANSACTIONS_CSV = os.path.join(DATA_DIR, "transactions.csv")


# Predefined 50 realistic courses across all 8 required categories
COURSES_DATA = [
    # Technology (10 courses)
    {"CourseID": "C001", "CourseName": "Python for Data Science and Machine Learning", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C002", "CourseName": "Complete Web Development Bootcamp: HTML, CSS, JavaScript", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C003", "CourseName": "Introduction to Python Programming", "CourseCategory": "Technology", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C004", "CourseName": "Cloud Computing Essentials with AWS", "CourseCategory": "Technology", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C005", "CourseName": "Deep Learning with PyTorch and TensorFlow", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Advanced"},
    {"CourseID": "C006", "CourseName": "Cybersecurity Fundamentals & Ethical Hacking", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C007", "CourseName": "Mobile App Development with Flutter & Dart", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C008", "CourseName": "DevOps & CI/CD Pipelines with Docker and Kubernetes", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Advanced"},
    {"CourseID": "C009", "CourseName": "Relational Database Design and SQL Mastery", "CourseCategory": "Technology", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C010", "CourseName": "Artificial Intelligence Architecture & System Design", "CourseCategory": "Technology", "CourseType": "Paid", "CourseLevel": "Advanced"},

    # Business (8 courses)
    {"CourseID": "C011", "CourseName": "Financial Modeling & Corporate Valuation in Excel", "CourseCategory": "Business", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C012", "CourseName": "Digital Marketing Strategy & SEO Fundamentals", "CourseCategory": "Business", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C013", "CourseName": "Project Management Principles & Agile Methodologies", "CourseCategory": "Business", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C014", "CourseName": "Entrepreneurship: From Idea Validation to Launch", "CourseCategory": "Business", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C015", "CourseName": "Strategic Management and Global Corporate Leadership", "CourseCategory": "Business", "CourseType": "Paid", "CourseLevel": "Advanced"},
    {"CourseID": "C016", "CourseName": "Professional Scrum Master (PSM) Certification Prep", "CourseCategory": "Business", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C017", "CourseName": "Product Management: From Discovery to Market Fit", "CourseCategory": "Business", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C018", "CourseName": "Global Supply Chain Logistics and Procurement", "CourseCategory": "Business", "CourseType": "Paid", "CourseLevel": "Intermediate"},

    # Science (6 courses)
    {"CourseID": "C019", "CourseName": "Introduction to Astronomy & Planetary Exploration", "CourseCategory": "Science", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C020", "CourseName": "General Chemistry: Atoms, Reactions, and Stoichiometry", "CourseCategory": "Science", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C021", "CourseName": "Genetics, Genomics, and Modern Biotechnology", "CourseCategory": "Science", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C022", "CourseName": "Environmental Science, Renewable Energy & Sustainability", "CourseCategory": "Science", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C023", "CourseName": "Quantum Physics Principles & Modern Mechanics", "CourseCategory": "Science", "CourseType": "Paid", "CourseLevel": "Advanced"},
    {"CourseID": "C024", "CourseName": "Cognitive Neuroscience: Unraveling the Brain", "CourseCategory": "Science", "CourseType": "Paid", "CourseLevel": "Intermediate"},

    # Arts (6 courses)
    {"CourseID": "C025", "CourseName": "Graphic Design Masterclass: Photoshop, Illustrator, InDesign", "CourseCategory": "Arts", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C026", "CourseName": "Digital Photography: Composition, Lighting, and Exposure", "CourseCategory": "Arts", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C027", "CourseName": "UI/UX Design Essentials: Wireframing and Prototyping in Figma", "CourseCategory": "Arts", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C028", "CourseName": "Music Theory, Harmony, and Contemporary Songwriting", "CourseCategory": "Arts", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C029", "CourseName": "Digital Painting and Character Concept Art", "CourseCategory": "Arts", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C030", "CourseName": "Screenwriting & Narrative Storytelling for Film and Media", "CourseCategory": "Arts", "CourseType": "Paid", "CourseLevel": "Intermediate"},

    # Health (5 courses)
    {"CourseID": "C031", "CourseName": "Nutritional Science, Metabolism, and Dietary Wellness", "CourseCategory": "Health", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C032", "CourseName": "Foundations of Mental Health, Stress Resilience & Mindfulness", "CourseCategory": "Health", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C033", "CourseName": "Human Anatomy, Physiology, and Biomechanics", "CourseCategory": "Health", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C034", "CourseName": "Public Health Policy, Epidemiology, and Disease Control", "CourseCategory": "Health", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C035", "CourseName": "Strength Conditioning & Exercise Physiology", "CourseCategory": "Health", "CourseType": "Paid", "CourseLevel": "Beginner"},

    # Mathematics (5 courses)
    {"CourseID": "C036", "CourseName": "Linear Algebra, Vectors, and Matrices for Machine Learning", "CourseCategory": "Mathematics", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C037", "CourseName": "Calculus I: Limits, Derivatives, and Applications", "CourseCategory": "Mathematics", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C038", "CourseName": "Probability and Applied Statistics for Data Analysis", "CourseCategory": "Mathematics", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C039", "CourseName": "Discrete Mathematics for Computer Science & Cryptography", "CourseCategory": "Mathematics", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C040", "CourseName": "Multivariable Calculus and Partial Differential Equations", "CourseCategory": "Mathematics", "CourseType": "Paid", "CourseLevel": "Advanced"},

    # Language (5 courses)
    {"CourseID": "C041", "CourseName": "Spanish for Beginners: Practical Conversational Fluency", "CourseCategory": "Language", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C042", "CourseName": "Intermediate Spanish: Grammar Mastery & Cultural Context", "CourseCategory": "Language", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C043", "CourseName": "Business English: International Negotiations & Presentations", "CourseCategory": "Language", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C044", "CourseName": "French Language & Culture for Beginners", "CourseCategory": "Language", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C045", "CourseName": "Japanese Foundations: Hiragana, Katakana, and Essential Kanji", "CourseCategory": "Language", "CourseType": "Paid", "CourseLevel": "Beginner"},

    # Personal Development (5 courses)
    {"CourseID": "C046", "CourseName": "High-Performance Time Management and Deep Work Habits", "CourseCategory": "Personal Development", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C047", "CourseName": "Mastering Public Speaking & Executive Presence", "CourseCategory": "Personal Development", "CourseType": "Paid", "CourseLevel": "Beginner"},
    {"CourseID": "C048", "CourseName": "Critical Thinking, Logic, and Creative Problem Solving", "CourseCategory": "Personal Development", "CourseType": "Free", "CourseLevel": "Beginner"},
    {"CourseID": "C049", "CourseName": "Emotional Intelligence, Empathy & High-Trust Relationships", "CourseCategory": "Personal Development", "CourseType": "Paid", "CourseLevel": "Intermediate"},
    {"CourseID": "C050", "CourseName": "Strategic Career Navigation, Mentorship & Salary Negotiation", "CourseCategory": "Personal Development", "CourseType": "Paid", "CourseLevel": "Advanced"},
]


def load_or_create_users(users_csv_path: str = USERS_CSV) -> pd.DataFrame:
    """
    Load users.csv if it exists; otherwise automatically generate it
    using create_users_csv.py.
    """
    if not os.path.exists(users_csv_path):
        print(f"Users dataset not found at {users_csv_path}. Generating users.csv...")
        try:
            import create_users_csv
            create_users_csv.main(users_csv_path)
        except ImportError:
            # Fallback inline generation if create_users_csv module import fails
            print("Import fallback: Generating users inline...")
            from create_users_csv import generate_users, save_users_csv
            users_list = generate_users(3000, seed=42)
            save_users_csv(users_list, users_csv_path)

    df_users = pd.read_csv(users_csv_path)
    print(f"Loaded {len(df_users)} users from {users_csv_path}")
    return df_users


def generate_courses_csv(output_path: str = COURSES_CSV) -> pd.DataFrame:
    """Save the predefined 50 courses to courses.csv."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    df_courses = pd.DataFrame(COURSES_DATA)
    df_courses.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Successfully generated and saved {len(df_courses)} courses to {output_path}")
    return df_courses


def calculate_course_weights(df_courses: pd.DataFrame) -> np.ndarray:
    """
    Compute popularity probability weights for courses based on:
    - Level (Beginner courses are more popular)
    - Type (Free courses have slight preference)
    - Category (Technology and Business have higher demand)
    """
    weights = []
    level_multiplier = {
        "Beginner": 2.5,
        "Intermediate": 1.4,
        "Advanced": 0.6
    }
    type_multiplier = {
        "Free": 1.35,
        "Paid": 1.0
    }
    category_multiplier = {
        "Technology": 1.6,
        "Business": 1.4,
        "Arts": 1.1,
        "Health": 1.0,
        "Mathematics": 0.95,
        "Language": 0.95,
        "Science": 0.85,
        "Personal Development": 1.05
    }

    for _, row in df_courses.iterrows():
        w = (
            level_multiplier.get(row["CourseLevel"], 1.0)
            * type_multiplier.get(row["CourseType"], 1.0)
            * category_multiplier.get(row["CourseCategory"], 1.0)
        )
        weights.append(w)

    weights = np.array(weights, dtype=float)
    return weights / weights.sum()


def generate_transactions(
    df_users: pd.DataFrame,
    df_courses: pd.DataFrame,
    target_count: int = 6500,
    seed: int = 42,
    output_path: str = TRANSACTIONS_CSV
) -> pd.DataFrame:
    """
    Generate synthetic transactions between 2023-01-01 and 2024-12-31.
    
    Distribution characteristics:
    - Seed 42 for reproducibility
    - Younger users (15-24) have higher enrollment rates and higher transaction counts
    - Not all users make transactions (~75% active users)
    - Realistic course popularity weighting (Beginner > Intermediate > Advanced)
    - No duplicate course purchases for a single user
    - Dates smoothly distributed across the 2-year window with seasonal peaks
    """
    np.random.seed(seed)
    random.seed(seed)

    course_weights = calculate_course_weights(df_courses)
    course_ids = df_courses["CourseID"].tolist()
    num_courses = len(course_ids)

    # Date range: 2023-01-01 to 2024-12-31 (731 days)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days + 1

    # Determine user activity probabilities based on age
    user_records = []
    for _, user in df_users.iterrows():
        uid = str(user["UserID"])
        age = int(user["Age"])
        
        # Younger users are more likely to participate
        if age <= 21:
            active_prob = 0.85
            max_courses = 6
        elif age <= 28:
            active_prob = 0.78
            max_courses = 5
        else:
            active_prob = 0.65
            max_courses = 3

        if random.random() < active_prob:
            # Pick number of courses this user takes (weighted towards 1-3 courses)
            probs = [0.45, 0.28, 0.15, 0.08, 0.03, 0.01][:max_courses]
            probs = np.array(probs) / sum(probs)
            num_tx = np.random.choice(range(1, len(probs) + 1), p=probs)
            user_records.append((uid, age, num_tx))

    # Scale or sample transactions to hit target range (5000 - 8000)
    raw_total = sum(tx_count for _, _, tx_count in user_records)
    scaling_ratio = target_count / raw_total

    transactions = []
    tx_counter = 1

    for uid, age, num_tx in user_records:
        # Probabilistically adjust count according to scaling_ratio
        actual_num_tx = int(num_tx * scaling_ratio)
        if random.random() < (num_tx * scaling_ratio - actual_num_tx):
            actual_num_tx += 1
            
        actual_num_tx = max(1, min(actual_num_tx, num_courses))

        # Sample distinct courses without replacement for this user
        chosen_courses = np.random.choice(
            course_ids,
            size=actual_num_tx,
            replace=False,
            p=course_weights
        )

        # Generate timestamps for each course purchase
        # Distinct or ordered dates for realistic user behavior
        days_offsets = sorted(np.random.randint(0, total_days, size=actual_num_tx))
        for course_id, day_offset in zip(chosen_courses, days_offsets):
            tx_date = start_date + timedelta(days=int(day_offset))
            # Add realistic hours, minutes, seconds
            hour = random.randint(8, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            full_tx_date = tx_date.replace(hour=hour, minute=minute, second=second)

            transactions.append({
                "TransactionID": f"T{tx_counter:05d}",
                "UserID": uid,
                "CourseID": course_id,
                "TransactionDate": full_tx_date.strftime("%Y-%m-%d %H:%M:%S")
            })
            tx_counter += 1

    # Sort transactions chronologically
    transactions.sort(key=lambda x: x["TransactionDate"])

    # Re-assign sequential TransactionIDs after sorting
    for idx, tx in enumerate(transactions, start=1):
        tx["TransactionID"] = f"T{idx:05d}"

    df_transactions = pd.DataFrame(transactions)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    df_transactions.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Successfully generated and saved {len(df_transactions)} transactions to {output_path}")
    print(f"Active Users with transactions: {df_transactions['UserID'].nunique()} / {len(df_users)}")
    print(f"Date range: {df_transactions['TransactionDate'].min()[:10]} to {df_transactions['TransactionDate'].max()[:10]}")
    return df_transactions


def main():
    """Main execution orchestrator."""
    print("=" * 60)
    print("Starting EduPro Data Generation (Seed: 42)")
    print("=" * 60)

    # 1. Ensure / load users.csv
    df_users = load_or_create_users(USERS_CSV)

    # 2. Generate courses.csv (50 courses)
    df_courses = generate_courses_csv(COURSES_CSV)

    # 3. Generate transactions.csv (5,000 - 8,000 transactions)
    df_transactions = generate_transactions(
        df_users=df_users,
        df_courses=df_courses,
        target_count=6800,
        seed=42,
        output_path=TRANSACTIONS_CSV
    )

    print("=" * 60)
    print("Data Generation Complete!")
    print(f"- Users: {len(df_users)} records -> {USERS_CSV}")
    print(f"- Courses: {len(df_courses)} records -> {COURSES_CSV}")
    print(f"- Transactions: {len(df_transactions)} records -> {TRANSACTIONS_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    main()
