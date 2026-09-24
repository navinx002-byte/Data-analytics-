import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1280
HEIGHT = 720
FPS = 24
SECONDS_PER_SLIDE = 8

slides_data = [
    {
        "title": "EduPro Learner Analytics",
        "subtitle": "Demographics & Course Enrollment Behavior Analysis",
        "author": "Author: Navin D | Unified Mentor Internship",
        "bullets": [
            "Comprehensive empirical study of online learning platform behavior",
            "Dataset: 3,000 Learners | 50 Courses (8 Domains) | 6,803 Enrollments",
            "Interactive Streamlit Dashboard & Complete Research Documentation",
            "Live Web App: https://navinx002-byte-data-analytics.streamlit.app"
        ],
        "badge": "PROJECT OVERVIEW & INTRODUCTION"
    },
    {
        "title": "Platform Key Performance Indicators",
        "subtitle": "High-Level Engagement & Demographics Summary",
        "author": "EduPro Learner Intelligence Platform",
        "bullets": [
            "Total Registered Learners: 3,000 (Ages 15 - 35)",
            "Active Enrolled Learners: 2,288 (76.3% engagement rate)",
            "Total Enrollment Transactions: 6,803 records (2023 - 2024)",
            "Gender Participation Ratio: 50.9% Male to 49.1% Female (Near Parity)",
            "Course Consumption Velocity: Average 2.99 courses per active user"
        ],
        "badge": "EXECUTIVE KPI DASHBOARD"
    },
    {
        "title": "Demographic & Enrollment Findings",
        "subtitle": "Age Bands, Course Categories & Skill Levels",
        "author": "Exploratory Data Analysis Insights",
        "bullets": [
            "Dominant Age Cohort: 18-25 bracket represents the highest course velocity",
            "Top Subject Domains: Technology (26.4%) and Business (21.7%) lead demand",
            "Skill Tier Distribution: Beginner courses account for 47.8% of all enrollments",
            "Pricing Model: Paid courses capture 58.2% vs. 41.8% Free courses",
            "Gender Topical Disparity: Negligible variance (<3%) across STEM disciplines"
        ],
        "badge": "KEY ANALYTICAL FINDINGS"
    },
    {
        "title": "Interactive Streamlit Web Dashboard",
        "subtitle": "Live Cloud Analytics Features & User Capabilities",
        "author": "Built with Python, Streamlit, Pandas & Plotly",
        "bullets": [
            "Tab 1: Overview & KPIs - Live metrics, age histogram, gender donut chart",
            "Tab 2: Learner Demographics - Age group stratification and gender splits",
            "Tab 3: Enrollment Behavior - Category bar charts and monthly trend timeline",
            "Tab 4: Demographics x Courses - Heatmap matrix and cross-tabulation",
            "Tab 5: Behavioral Insights - Active user concentration and skill levels",
            "Tab 6: Data Explorer - Interactive table viewer with CSV download"
        ],
        "badge": "DASHBOARD ARCHITECTURE & MODULES"
    },
    {
        "title": "Strategic Recommendations & Learnings",
        "subtitle": "Actionable Takeaways for Education Stakeholders",
        "author": "Conclusions & Vocational Pathway Design",
        "bullets": [
            "Curriculum Depth: Build intermediate tracks to graduate the 47.8% beginner base",
            "Career Specializations: Bundle related tech & management skills with certifications",
            "Targeted Engagement: Design preparatory coding/language modules for <18 learners",
            "Technical Growth: Gained mastery in end-to-end data analytics and web deployment",
            "GitHub Repository: https://github.com/navinx002-byte/Data-analytics-"
        ],
        "badge": "RECOMMENDATIONS & CONCLUSION"
    }
]

def create_slide_image(data):
    # Dark modern canvas
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(18, 24, 38))
    draw = ImageDraw.Draw(img)

    # Accent top bar
    draw.rectangle([0, 0, WIDTH, 8], fill=(31, 119, 180))

    # Badge pill
    draw.rectangle([60, 45, 480, 80], fill=(26, 44, 76), outline=(41, 128, 185), width=1)
    draw.text((80, 52), data["badge"], fill=(100, 181, 246))

    # Main Title
    draw.text((60, 105), data["title"], fill=(255, 255, 255))
    draw.text((60, 160), data["subtitle"], fill=(176, 190, 197))
    draw.text((60, 200), data["author"], fill=(79, 195, 247))

    # Divider line
    draw.line([60, 235, WIDTH - 60, 235], fill=(55, 71, 79), width=2)

    # Bullet points
    y = 275
    for i, b in enumerate(data["bullets"]):
        # Bullet dot
        draw.ellipse([70, y + 6, 82, y + 18], fill=(0, 230, 118))
        draw.text((105, y), b, fill=(236, 239, 241))
        y += 72

    # Footer bar
    draw.rectangle([0, HEIGHT - 55, WIDTH, HEIGHT], fill=(13, 17, 28))
    draw.text((60, HEIGHT - 40), "🎓 EduPro Analytics Project | Navin D | Unified Mentor", fill=(144, 164, 174))
    draw.text((WIDTH - 420, HEIGHT - 40), "Live: navinx002-byte-data-analytics.streamlit.app", fill=(79, 195, 247))

    return np.array(img)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "project_walkthrough.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))

total_frames = 0
for slide in slides_data:
    frame_rgb = create_slide_image(slide)
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    for _ in range(FPS * SECONDS_PER_SLIDE):
        out.write(frame_bgr)
        total_frames += 1

out.release()
print(f"✅ Video created successfully: {output_path} ({total_frames} frames, {total_frames/FPS:.1f}s)")
