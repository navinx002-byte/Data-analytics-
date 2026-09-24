# Learner Demographics and Course Enrollment Behavior Analysis on EduPro

**Author:** Navin D  
**Affiliation:** Unified Mentor Internship Program  
**Domain:** Educational Data Mining & Platform Analytics  
**Date:** September 2026  
**Repository:** [https://github.com/navinx002-byte/Data-analytics-](https://github.com/navinx002-byte/Data-analytics-)  
**Live Application:** [https://navinx002-byte-data-analytics.streamlit.app](https://navinx002-byte-data-analytics.streamlit.app)  

---

## Abstract

Online learning platforms cater to increasingly diverse learner cohorts spanning heterogeneous age brackets, vocational orientations, and pedagogical backgrounds. This study presents a descriptive analytics framework examining learner demographics and enrollment behavior on EduPro, an emerging digital education platform. Analyzing multi-relational transactional data comprising 3,000 registered users, 50 catalog courses across 8 subject domains, and 6,839 enrollment instances spanning 2023–2024, we investigate: (i) demographic reach across age and gender segments, (ii) subject category preferences, (iii) course difficulty level distribution, and (iv) behavioral intensity among active users. 

Key empirical findings indicate a near parity in gender participation (51.1% Male vs. 48.9% Female), with strong enrollment concentration in Technology (26.4%) and Business (21.7%) disciplines. Furthermore, beginner-tier courses capture over 47.8% of aggregate demand, particularly among learners aged 15–25. The platform exhibits a healthy engagement profile with an average of 2.99 courses completed per active user. We distill these empirical observations into four strategic pillars for platform administrators: targeted course commissioning, demographic-tailored curriculum tracks, tiered pricing strategies, and inclusive learner retention initiatives.

---

## 1. Introduction

Online education platforms have evolved from supplementary instructional repositories into primary educational environments for vocational training, credential acquisition, and lifelong learning. Central to the sustainable expansion of modern EdTech ecosystems is **Learner Intelligence**—the systematic extraction of behavioral, demographic, and transactional signals to inform educational product strategy.

EduPro serves a broad learner constituency spanning secondary school students, university undergraduates, early-career entrants, and mid-career transitioning professionals. While platform usage metrics reflect continuous user registration, prior operational choices have largely relied on anecdotal assumptions rather than rigorous empirical discovery. This investigation addresses this gap by executing a descriptive data intelligence protocol focusing on non-monetary, pedagogy-first behavioral dimensions.

---

## 2. Problem Statement

Despite capturing comprehensive relational records encompassing user profiles, course catalog metadata, and enrollment transactions, EduPro previously lacked formalized answers to core strategic questions:

1. **Demographic Concentration:** What is the underlying age structure of EduPro's registered cohort, and which cohorts drive platform enrollment?
2. **Gender Parity:** Do gender-based variances manifest in course topic selection, level difficulty preference, or course pricing sensitivity?
3. **Curricular Affinity:** Which subject categories command primary interest across adolescent (<18), young adult (18–25), and professional (26–35) learners?
4. **Skill Maturity Profile:** Does demand skew toward fundamental/beginner training, or do users actively consume advanced, specialized courseware?

Without empirically validated answers, institutional resource allocation—such as instructor recruitment, syllabus drafting, and promotional outreach—remains speculative.

---

## 3. Dataset Architecture & Verification

The study leverages three interconnected relational datasets integrated through primary-foreign key relationships:

### 3.1 Schema Overview

| Dataset | Dimensions | Primary Key | Foreign Keys | Key Attributes |
| :--- | :--- | :--- | :--- | :--- |
| **Users** | 3,000 × 5 | `UserID` | — | `UserName`, `Age` (15–35), `Gender`, `Email` |
| **Courses** | 50 × 5 | `CourseID` | — | `CourseName`, `CourseCategory` (8 domains), `CourseType` (Free/Paid), `CourseLevel` (Beginner/Intermediate/Advanced) |
| **Transactions** | 6,839 × 4 | `TransactionID` | `UserID`, `CourseID` | `TransactionDate` (2023-01-01 to 2024-12-31) |

### 3.2 Subject Domain Breakdown
The catalog of 50 courses encompasses 8 distinct disciplines:
- **Technology (8 courses):** Python, Web Development, Data Science, Machine Learning, Cloud Computing, Cybersecurity, Mobile Development, AI.
- **Business (6 courses):** Entrepreneurship, Digital Marketing, Financial Accounting, Project Management, Business Analytics, Leadership.
- **Science (5 courses):** Biology, Chemistry, Physics, Environmental Science, Astronomy.
- **Arts (5 courses):** Graphic Design, Photography, Creative Writing, Music Production, Video Editing.
- **Health (5 courses):** Nutrition & Wellness, Mental Health, First Aid, Yoga/Mindfulness, Public Health.
- **Mathematics (4 courses):** Statistics & Probability, Calculus, Linear Algebra, Discrete Math.
- **Language (5 courses):** English Grammar, Spanish, French, Japanese, Public Speaking.
- **Personal Development (4 courses):** Time Management, Critical Thinking, Emotional Intelligence, Resume & Career Strategy.

---

## 4. Methodology

```
[Raw Relational Tables] ───► [Data Integration & Referencing] ───► [Demographic Segmentation]
  - Users (3,000)               - Inner Join on UserID & CourseID     - Age Bands: <18, 18-25, 26-35
  - Courses (50)                - Temporal parsing (YYYY-MM)           - Gender Categorization
  - Transactions (6,839)
                                          │
                                          ▼
[Interactive Dashboard UI] ◄── [Descriptive Intelligence] ◄── [Cross-Tabulation & KPI Extraction]
  - 5 Dedicated Views             - Course Demand Ranking       - Age × Category Heatmap
  - Dynamic Multiselects          - Level Affinity Ratios       - Gender × Level Stacked Dist.
  - Plotly Visualizations         - User Concentration Models   - Monthly Trajectory Analysis
```

1. **Referential Integrity Validation:** Verified zero orphan transactions; 100% of transaction `UserID` and `CourseID` values map to canonical user and course definitions.
2. **Cohort Stratification:** Binned age into three actionable educational bands:
   - **Under 18 (Secondary School):** Ages 15–17 (focus on foundational orientation).
   - **18–25 (Higher Education & Job Entry):** Ages 18–25 (career preparation).
   - **26–35 (Working Professionals):** Ages 26–35 (skill upgrading & lateral shifts).
3. **Multi-dimensional Crosstabulation:** Matrix formulation evaluating `Age Group × Category`, `Gender × Level`, and `Category × CourseType`.

---

## 5. Empirical Findings & Analysis

### 5.1 Demographic Composition
- **Active User Rate:** Of 3,000 registered accounts, **2,284 users (76.1%)** executed at least one course enrollment within the 24-month observation window.
- **Age Distribution:** Uniform representation across ages 15–35 (mean: 25.1 years, median: 25 years, standard deviation: 6.07 years).
- **Gender Ratio:** 1,163 active male learners to 1,121 active female learners (**50.9% Male : 49.1% Female**), indicating an exceptionally balanced platform intake.

### 5.2 Category Popularity & Enrollment Demand

| Category | Courses Available | Total Enrollments | Share of Total | Popularity Index |
| :--- | :--- | :--- | :--- | :--- |
| **Technology** | 8 | 1,805 | 26.4% | 1.32 (High) |
| **Business** | 6 | 1,482 | 21.7% | 1.25 (High) |
| **Science** | 5 | 794 | 11.6% | 0.98 (Moderate) |
| **Health** | 5 | 751 | 11.0% | 0.95 (Moderate) |
| **Language** | 5 | 698 | 10.2% | 0.91 (Moderate) |
| **Arts** | 5 | 582 | 8.5% | 0.77 (Moderate) |
| **Personal Development** | 4 | 431 | 6.3% | 0.74 (Lower) |
| **Mathematics** | 4 | 296 | 4.3% | 0.58 (Niche) |
| **Total** | **50** | **6,839** | **100.0%** | **1.00** |

*Technology and Business alone constitute 48.1% of all platform activity, driven by professional marketability and career transformation aspirations.*

### 5.3 Course Level & Pricing Affinity
- **Level Distribution:**
  - **Beginner:** 3,272 enrollments (**47.8%**)
  - **Intermediate:** 2,462 enrollments (**36.0%**)
  - **Advanced:** 1,105 enrollments (**16.2%**)
  The heavy skew toward Beginner courseware confirms EduPro acts primarily as a point-of-entry onboarding platform for new skill domains.
- **Pricing Split:** Paid offerings account for 58.2% of enrollments, with Free introductory modules accounting for 41.8%, exhibiting healthy learner readiness to invest in structured learning.

### 5.4 Demographics × Preference Correlations
- **Adolescent Learners (<18):** Over-index in introductory Technology (Python, Web Development) and Language modules.
- **Undergraduate & Graduate Demographic (18–25):** Demonstrates the highest aggregate volume, heavily consuming Applied Machine Learning, Cloud Infrastructure, and Business Analytics.
- **Working Professionals (26–35):** Concentrate on Leadership, Financial Accounting, Project Management, and Advanced Technical Specializations.
- **Gender Disaggregation:** Gender differences in topical choice are negligible (<3% variance across STEM categories), reflecting broad inclusivity in modern digital educational platform access.

### 5.5 User Engagement & Concentration
- Average courses completed per active learner: **2.99 courses**.
- Top 10% of learners account for **24.8%** of total platform enrollments, demonstrating a dedicated core learner cohort.
- Maximum courses completed by a single learner: **9 courses**.

---

## 6. Key Performance Indicators (KPI Summary)

| Metric | Measured Value | Strategic Benchmark Interpretation |
| :--- | :--- | :--- |
| **Total Registered Users** | 3,000 | Healthy user acquisition base |
| **Active Enrolled Learners** | 2,284 (76.1%) | Superior onboarding conversion |
| **Total Course Enrollments** | 6,839 | Strong multi-enrollment adoption |
| **Catalog Breadth** | 50 Courses | Balanced foundational coverage |
| **Mean Courses / User** | 2.99 | High retention & platform stickiness |
| **Gender Participation Index** | 50.9% M / 49.1% F | Parity benchmark achieved |
| **Primary Domain Lead** | Technology (26.4%) | Dominant student acquisition vehicle |
| **Skill Tier Foundation** | 47.8% Beginner | Pipeline feeding into advanced stages |

---

## 7. Strategic Recommendations for EduPro Stakeholders

1. **Curricular Depth in Tech & Management:** Expand intermediate and advanced sequences in Technology and Business to create upward pathways for the 47.8% beginner base.
2. **K-12 & Pre-University Pathways:** Develop specialized preparatory learning tracks targeting the <18 demographic (e.g., Coding for High School, College Readiness).
3. **Cohort-Specific Pricing & Bundling:** Bundle beginner + intermediate courses into vocational specialization tracks with milestone certifications.
4. **Mathematics & Foundational Sciences Revamp:** Apply contextualized learning (e.g., "Math for Machine Learning" or "Statistics for Business Decisions") to revive demand in low-uptake categories.

---

## 8. Conclusion

This empirical investigation provides foundational, data-backed intelligence regarding the demographic footprint and consumption behaviors of EduPro's user population. Rather than relying on speculative intuition, platform leadership can now steer curriculum design, instructor recruitment, and promotional resources with precision. 

---

## 9. References

1. Baker, R. S., & Inventado, P. S. (2014). Educational Data Mining and Learning Analytics. In *Learning Analytics* (pp. 61-75). Springer, New York, NY.
2. Ferguson, R. (2012). The State of Learning Analytics in 2012: A Review and Future Challenges. *Knowledge Technologies Media*, 1(1), 1-17.
3. Siemens, G. (2013). Learning Analytics: The Emergence of a Discipline. *American Behavioral Scientist*, 57(10), 1380-1400.
4. Romero, C., & Ventura, S. (2020). Educational Data Mining and Learning Analytics: An Updated Survey. *WIREs Data Mining and Knowledge Discovery*, 10(3), e1355.
5. Kizilcec, R. F., Piech, C., & Schneider, E. (2013). Deconstructing Disengagement: Analyzing Learner Subpopulations in Massive Open Online Courses. *Proceedings of the Third International Conference on Learning Analytics and Knowledge*, 170-179.
