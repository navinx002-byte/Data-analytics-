# 🎓 Learner Demographics and Course Enrollment Behavior Analysis on EduPro

## 📋 Project Overview

This project provides a comprehensive analysis of learner demographics and course enrollment behavior on the **EduPro** online learning platform. By systematically analyzing who the learners are and how they enroll, EduPro can move toward data-driven education planning.

### Key Objectives
- Understand the age and gender distribution of learners
- Analyze course enrollment patterns across demographics
- Identify course category preferences by learner segments
- Provide actionable insights for course design and marketing

## 📊 Dataset

| Sheet | Records | Key Fields |
|-------|---------|------------|
| Users | 3,000 | UserID, UserName, Age, Gender, Email |
| Courses | 50 | CourseID, CourseName, CourseCategory, CourseType, CourseLevel |
| Transactions | 6,839 | TransactionID, UserID, CourseID, TransactionDate |

### Course Categories
Technology, Business, Science, Arts, Health, Mathematics, Language, Personal Development

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/navinx002-byte/Data-analytics-.git
cd Data-analytics-

# Install dependencies
pip install -r requirements.txt
```

### Generate Data (if needed)
```bash
python create_users_csv.py
python generate_data.py
```

### Run the Dashboard
```bash
streamlit run app.py
```

## 📈 Dashboard Features

### Tab 1: Overview
- KPI cards (Total Learners, Enrollments, Courses, Avg Courses/Learner, Gender Ratio)
- Age distribution histogram
- Gender distribution pie chart

### Tab 2: Learner Demographics
- Age distribution by gender
- Age band distribution
- Gender split within age groups

### Tab 3: Enrollment Analysis
- Course category popularity
- Free vs Paid enrollment split
- Course level distribution
- Monthly enrollment trends
- Most/Least popular courses

### Tab 4: Demographics × Course Preferences
- Age Group vs Course Category heatmap
- Gender vs Course Level comparison
- Gender vs Course Category analysis

### Tab 5: Behavioral Insights
- Course enrollment distribution per learner
- Top 10 most active learners
- Course level preferences by age group

## 🔍 Key Analytical Questions Answered

1. What is the age distribution of learners on EduPro?
2. How does course enrollment vary across age groups?
3. Are there gender-based differences in course selection?
4. Which course categories attract the highest enrollments?
5. Do beginners prefer certain course types or levels?

## 🛠️ Tech Stack

- **Python** - Data processing and analysis
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **Streamlit** - Web application framework
- **NumPy** - Numerical computing

## 📁 Project Structure

```
├── app.py                  # Streamlit dashboard
├── generate_data.py        # Synthetic data generator
├── create_users_csv.py     # User data generator
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── data/
    ├── users.csv           # Learner demographics
    ├── courses.csv         # Course catalog
    └── transactions.csv    # Enrollment records
```

## 📊 KPIs Tracked

| KPI | Description |
|-----|-------------|
| Total Enrollments | Platform engagement indicator |
| Enrollments by Age Group | Demographic reach |
| Gender Participation Ratio | Inclusivity metric |
| Category Popularity Index | Course demand |
| Level Preference Distribution | Skill maturity insight |

## 👤 Author

**Navin D** - Data Analytics Project

## 📄 License

This project is for educational and analytical purposes.
