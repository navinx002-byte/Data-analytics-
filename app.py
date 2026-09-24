import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(
    page_title="EduPro Analytics - Learner Demographics & Enrollments",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme helper for Plotly ---
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="sans-serif"),
    margin=dict(l=40, r=40, t=50, b=40)
)
COLOR_PALETTE = px.colors.qualitative.Bold

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-container {
        border-radius: 8px;
        padding: 12px;
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    
    users_path = os.path.join(data_dir, 'users.csv')
    courses_path = os.path.join(data_dir, 'courses.csv')
    trans_path = os.path.join(data_dir, 'transactions.csv')
    
    if not (os.path.exists(users_path) and os.path.exists(courses_path) and os.path.exists(trans_path)):
        try:
            import generate_data
            generate_data.main()
        except Exception:
            pass

    users = pd.read_csv(users_path)
    courses = pd.read_csv(courses_path)
    transactions = pd.read_csv(trans_path)

    # Merge datasets
    df = pd.merge(transactions, users, on='UserID')
    df = pd.merge(df, courses, on='CourseID')
    
    # Create standardized Age Bands
    bins = [0, 18, 26, 36, 100]
    labels = ['Under 18', '18-25', '26-35', '36+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False).astype(str)
    
    # Date formatting
    if 'TransactionDate' in df.columns:
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['MonthYear'] = df['TransactionDate'].dt.to_period('M').dt.strftime('%Y-%m')
        
    return df, users, courses, transactions

df, users_df, courses_df, transactions_df = load_data()

# Ensure users dataframe also has Age Group
bins = [0, 18, 26, 36, 100]
labels = ['Under 18', '18-25', '26-35', '36+']
users_df['Age Group'] = pd.cut(users_df['Age'], bins=bins, labels=labels, right=False).astype(str)

# --- Sidebar Filters ---
st.sidebar.title("🎓 EduPro Intelligence")
st.sidebar.caption("Filter learners and course transactions")

# Reset button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    for key in ['sel_age', 'sel_gender', 'sel_cat', 'sel_lvl']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Filter options
all_ages = ['Under 18', '18-25', '26-35']
present_ages = [a for a in all_ages if a in df['Age Group'].unique()]
all_genders = sorted(df['Gender'].dropna().unique().tolist())
all_cats = sorted(df['CourseCategory'].dropna().unique().tolist())
all_lvls = ['Beginner', 'Intermediate', 'Advanced']
present_lvls = [lvl for lvl in all_lvls if lvl in df['CourseLevel'].unique()]

selected_age = st.sidebar.multiselect("Age Group", options=present_ages, default=present_ages, key="sel_age")
selected_gender = st.sidebar.multiselect("Gender", options=all_genders, default=all_genders, key="sel_gender")
selected_category = st.sidebar.multiselect("Course Category", options=all_cats, default=all_cats, key="sel_cat")
selected_level = st.sidebar.multiselect("Course Level", options=present_lvls, default=present_lvls, key="sel_lvl")

# Fallback: if user deselects all in a multiselect, default to all so dashboard never goes blank
eff_age = selected_age if selected_age else present_ages
eff_gender = selected_gender if selected_gender else all_genders
eff_category = selected_category if selected_category else all_cats
eff_level = selected_level if selected_level else present_lvls

# Apply filters
filtered_df = df[
    (df['Age Group'].isin(eff_age)) &
    (df['Gender'].isin(eff_gender)) &
    (df['CourseCategory'].isin(eff_category)) &
    (df['CourseLevel'].isin(eff_level))
]

st.sidebar.markdown("---")
st.sidebar.metric("Active Enrollments", f"{len(filtered_df):,}", f"of {len(df):,} total")
st.sidebar.caption("EduPro Learner Intelligence Platform • Unified Mentor")

# --- App Header ---
st.title("🎓 Learner Demographics & Course Enrollment Behavior")
st.markdown(
    "Comprehensive empirical analysis of **3,000 registered learners**, **50 courses**, "
    "and **6,800+ transactions** across 8 subject domains on EduPro."
)

with st.expander("▶️ Project Feedback & Walkthrough Video (Author: Navin D)", expanded=False):
    if os.path.exists("project_walkthrough.mp4"):
        st.video("project_walkthrough.mp4")
    else:
        st.info("Video walkthrough available on GitHub repository.")

# --- Navigation Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview & KPIs", 
    "👥 Learner Demographics", 
    "📚 Enrollment Behavior", 
    "🔥 Demographics × Courses", 
    "🧠 Behavioral Insights",
    "📋 Data Explorer"
])

# =========================================================================
# TAB 1: OVERVIEW & KPIS
# =========================================================================
with tab1:
    st.subheader("Key Performance Indicators (KPIs)")
    
    total_learners = filtered_df['UserID'].nunique()
    total_enrollments = len(filtered_df)
    total_courses = filtered_df['CourseID'].nunique()
    avg_courses_per_learner = (total_enrollments / total_learners) if total_learners > 0 else 0
    
    unique_users = filtered_df.drop_duplicates(subset=['UserID'])
    gender_counts = unique_users['Gender'].value_counts()
    males = gender_counts.get('Male', 0)
    females = gender_counts.get('Female', 0)
    gender_ratio = f"{males}M : {females}F" if (males + females) > 0 else "N/A"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Active Learners", f"{total_learners:,}")
    with col2:
        st.metric("Total Enrollments", f"{total_enrollments:,}")
    with col3:
        st.metric("Active Courses", f"{total_courses:,}")
    with col4:
        st.metric("Avg Courses / Learner", f"{avg_courses_per_learner:.2f}")
    with col5:
        st.metric("Gender Ratio", gender_ratio)
        
    st.markdown("---")
    
    # Row 1: Charts
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig_age = px.histogram(
            unique_users, 
            x="Age", 
            nbins=21,
            title="Learner Age Distribution (Ages 15-35)",
            color_discrete_sequence=["#1f77b4"]
        )
        fig_age.update_layout(**PLOTLY_LAYOUT, xaxis_title="Age (Years)", yaxis_title="Learner Count")
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col_chart2:
        fig_gender = px.pie(
            unique_users, 
            names="Gender", 
            title="Gender Participation Ratio",
            color="Gender",
            color_discrete_map={"Male": "#2ca02c", "Female": "#ff7f0e"},
            hole=0.45
        )
        fig_gender.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_gender, use_container_width=True)

    # Row 2: Prominent Data Tables & Category Overview
    st.markdown("### 📌 Executive Highlights & Data Representation")
    col_sub1, col_sub2 = st.columns([1, 1])
    
    with col_sub1:
        st.markdown("**Top 5 Most Popular Courses**")
        top5 = filtered_df.groupby(['CourseName', 'CourseCategory', 'CourseLevel']).size().reset_index(name='Enrollments')
        top5 = top5.sort_values('Enrollments', ascending=False).head(5).reset_index(drop=True)
        st.dataframe(top5, use_container_width=True)
        
    with col_sub2:
        st.markdown("**Enrollments by Subject Domain**")
        cat_summary = filtered_df['CourseCategory'].value_counts().reset_index()
        cat_summary.columns = ['Category', 'Enrollments']
        cat_summary['Share %'] = (cat_summary['Enrollments'] / len(filtered_df) * 100).round(1).astype(str) + '%'
        st.dataframe(cat_summary, use_container_width=True)

# =========================================================================
# TAB 2: LEARNER DEMOGRAPHICS
# =========================================================================
with tab2:
    st.subheader("Learner Demographic Composition")
    unique_users = filtered_df.drop_duplicates(subset=['UserID'])
    
    col1, col2 = st.columns(2)
    with col1:
        # Age distribution by gender
        age_gender_dist = unique_users.groupby(['Age Group', 'Gender']).size().reset_index(name='Count')
        fig_age_gender = px.bar(
            age_gender_dist, 
            x='Age Group', 
            y='Count', 
            color='Gender', 
            barmode='group',
            title='Age Group Stratification by Gender',
            color_discrete_map={"Male": "#1f77b4", "Female": "#e377c2"},
            category_orders={"Age Group": ["Under 18", "18-25", "26-35"]}
        )
        fig_age_gender.update_layout(**PLOTLY_LAYOUT, yaxis_title="Active Learners")
        st.plotly_chart(fig_age_gender, use_container_width=True)
        
        # Gender split % within age groups
        fig_split = px.bar(
            age_gender_dist,
            x='Age Group',
            y='Count',
            color='Gender',
            title='Gender Composition across Age Bands',
            barmode='stack',
            color_discrete_map={"Male": "#1f77b4", "Female": "#e377c2"},
            category_orders={"Age Group": ["Under 18", "18-25", "26-35"]}
        )
        fig_split.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_split, use_container_width=True)
        
    with col2:
        # Age band distribution
        age_band_dist = unique_users['Age Group'].value_counts().reset_index()
        age_band_dist.columns = ['Age Group', 'Count']
        fig_age_band = px.bar(
            age_band_dist,
            x='Age Group',
            y='Count',
            title='Total Learners per Age Band',
            color='Age Group',
            color_discrete_sequence=COLOR_PALETTE,
            category_orders={"Age Group": ["Under 18", "18-25", "26-35"]}
        )
        fig_age_band.update_layout(**PLOTLY_LAYOUT, yaxis_title="Learner Count")
        st.plotly_chart(fig_age_band, use_container_width=True)
        
        # Demographic Summary Table
        st.markdown("**Demographic Summary Table**")
        demo_summary = unique_users.groupby('Age Group').agg(
            Total_Learners=('UserID', 'count'),
            Mean_Age=('Age', 'mean'),
            Min_Age=('Age', 'min'),
            Max_Age=('Age', 'max')
        ).reset_index()
        demo_summary['Mean_Age'] = demo_summary['Mean_Age'].round(1)
        st.dataframe(demo_summary, use_container_width=True)

# =========================================================================
# TAB 3: ENROLLMENT BEHAVIOR
# =========================================================================
with tab3:
    st.subheader("Course Enrollment Dynamics")
    
    col1, col2 = st.columns(2)
    with col1:
        # Category enrollments
        cat_enrolls = filtered_df['CourseCategory'].value_counts().reset_index()
        cat_enrolls.columns = ['Category', 'Enrollments']
        fig_cat = px.bar(
            cat_enrolls, 
            y='Category', 
            x='Enrollments', 
            orientation='h',
            title='Total Enrollments by Course Category',
            color='Enrollments',
            color_continuous_scale="Blues"
        )
        fig_cat.update_layout(**PLOTLY_LAYOUT, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)
        
        # Course Level enrollments
        level_enrolls = filtered_df['CourseLevel'].value_counts().reindex(['Beginner', 'Intermediate', 'Advanced']).reset_index()
        level_enrolls.columns = ['Level', 'Enrollments']
        fig_level = px.bar(
            level_enrolls, 
            x='Level', 
            y='Enrollments',
            title='Enrollment Demand by Course Level',
            color='Level',
            color_discrete_map={"Beginner": "#2ca02c", "Intermediate": "#ff7f0e", "Advanced": "#d62728"}
        )
        fig_level.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_level, use_container_width=True)
        
    with col2:
        # Course Type (Free vs Paid)
        type_enrolls = filtered_df['CourseType'].value_counts().reset_index()
        type_enrolls.columns = ['Type', 'Enrollments']
        fig_type = px.pie(
            type_enrolls, 
            names='Type', 
            values='Enrollments',
            title='Pricing Preference: Free vs Paid Offerings',
            color='Type',
            color_discrete_map={"Free": "#17becf", "Paid": "#9467bd"},
            hole=0.4
        )
        fig_type.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_type, use_container_width=True)
        
        # Monthly enrollment timeline
        if 'MonthYear' in filtered_df.columns:
            monthly_trend = filtered_df.groupby('MonthYear').size().reset_index(name='Enrollments')
            monthly_trend = monthly_trend.sort_values('MonthYear')
            fig_trend = px.line(
                monthly_trend, 
                x='MonthYear', 
                y='Enrollments',
                title='Monthly Enrollment Trajectory (2023 - 2024)',
                markers=True,
                line_shape="spline"
            )
            fig_trend.update_layout(**PLOTLY_LAYOUT, xaxis_title="Month", yaxis_title="Enrollments")
            st.plotly_chart(fig_trend, use_container_width=True)
            
    # Most and Least Popular Courses
    st.markdown("### 🏆 Course Popularity Standings")
    course_pop = filtered_df.groupby(['CourseID', 'CourseName', 'CourseCategory', 'CourseLevel', 'CourseType']).size().reset_index(name='Enrollments')
    course_pop = course_pop.sort_values('Enrollments', ascending=False)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**Top 5 In-Demand Courses**")
        st.dataframe(course_pop.head(5).reset_index(drop=True), use_container_width=True)
    with col_t2:
        st.markdown("**5 Least Enrolled Courses (Growth Opportunities)**")
        st.dataframe(course_pop.tail(5).reset_index(drop=True), use_container_width=True)

# =========================================================================
# TAB 4: DEMOGRAPHICS × COURSES
# =========================================================================
with tab4:
    st.subheader("Cross-Tabulation: Demographics × Course Selection")
    
    col1, col2 = st.columns(2)
    with col1:
        # Age Group vs Category Heatmap
        age_cat = pd.crosstab(filtered_df['Age Group'], filtered_df['CourseCategory'])
        age_order = [a for a in ["Under 18", "18-25", "26-35"] if a in age_cat.index]
        if age_order:
            age_cat = age_cat.reindex(age_order)
            
        fig_heat = px.imshow(
            age_cat,
            title='Heatmap: Age Band vs Course Category Affinity',
            labels=dict(x="Subject Category", y="Age Group", color="Enrollments"),
            aspect="auto",
            color_continuous_scale="Viridis"
        )
        fig_heat.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # Gender vs Course Level
        gen_lvl = filtered_df.groupby(['Gender', 'CourseLevel']).size().reset_index(name='Enrollments')
        fig_gen_lvl = px.bar(
            gen_lvl,
            x='CourseLevel',
            y='Enrollments',
            color='Gender',
            barmode='group',
            title='Course Level Selection by Gender',
            color_discrete_map={"Male": "#1f77b4", "Female": "#e377c2"},
            category_orders={"CourseLevel": ["Beginner", "Intermediate", "Advanced"]}
        )
        fig_gen_lvl.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_gen_lvl, use_container_width=True)
        
    with col2:
        # Gender vs Course Category
        gen_cat = filtered_df.groupby(['Gender', 'CourseCategory']).size().reset_index(name='Enrollments')
        fig_gen_cat = px.bar(
            gen_cat,
            y='CourseCategory',
            x='Enrollments',
            color='Gender',
            barmode='group',
            orientation='h',
            title='Category Distribution by Gender',
            color_discrete_map={"Male": "#1f77b4", "Female": "#e377c2"}
        )
        fig_gen_cat.update_layout(**PLOTLY_LAYOUT, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_gen_cat, use_container_width=True)
        
        # Age Group vs Course Type
        age_type = filtered_df.groupby(['Age Group', 'CourseType']).size().reset_index(name='Enrollments')
        fig_age_type = px.bar(
            age_type,
            x='Age Group',
            y='Enrollments',
            color='CourseType',
            barmode='stack',
            title='Free vs Paid Enrollment Ratio by Age Band',
            color_discrete_map={"Free": "#17becf", "Paid": "#9467bd"},
            category_orders={"Age Group": ["Under 18", "18-25", "26-35"]}
        )
        fig_age_type.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_age_type, use_container_width=True)

# =========================================================================
# TAB 5: BEHAVIORAL INSIGHTS
# =========================================================================
with tab5:
    st.subheader("Learner Engagement & Behavioral Intensity")
    
    # Calculate enrollments per user
    user_counts = filtered_df.groupby(['UserID', 'UserName', 'Age', 'Age Group', 'Gender']).size().reset_index(name='Courses Taken')
    
    col1, col2 = st.columns(2)
    with col1:
        fig_hist_user = px.histogram(
            user_counts,
            x='Courses Taken',
            nbins=10,
            title='Distribution of Courses Taken per Active Learner',
            color_discrete_sequence=["#8c564b"]
        )
        fig_hist_user.update_layout(**PLOTLY_LAYOUT, xaxis_title="Courses Completed", yaxis_title="Number of Learners")
        st.plotly_chart(fig_hist_user, use_container_width=True)
        
        # Beginner vs Advanced % by Age Group
        age_lvl = filtered_df.groupby(['Age Group', 'CourseLevel']).size().reset_index(name='Count')
        age_tot = age_lvl.groupby('Age Group')['Count'].transform('sum')
        age_lvl['Percentage'] = (age_lvl['Count'] / age_tot * 100).round(1)
        
        fig_age_lvl_share = px.bar(
            age_lvl,
            x='Age Group',
            y='Percentage',
            color='CourseLevel',
            title='Relative Course Level Distribution by Age Group (%)',
            barmode='stack',
            color_discrete_map={"Beginner": "#2ca02c", "Intermediate": "#ff7f0e", "Advanced": "#d62728"},
            category_orders={"Age Group": ["Under 18", "18-25", "26-35"]}
        )
        fig_age_lvl_share.update_layout(**PLOTLY_LAYOUT, yaxis_title="Percentage (%)")
        st.plotly_chart(fig_age_lvl_share, use_container_width=True)
        
    with col2:
        st.markdown("**Top 10 Most Active Power Learners**")
        top10 = user_counts.sort_values('Courses Taken', ascending=False).head(10).reset_index(drop=True)
        st.dataframe(top10[['UserID', 'UserName', 'Age', 'Gender', 'Courses Taken']], use_container_width=True)
        
        avg_by_age = user_counts.groupby('Age Group')['Courses Taken'].mean().reset_index()
        avg_by_age['Courses Taken'] = avg_by_age['Courses Taken'].round(2)
        fig_avg_age = px.bar(
            avg_by_age,
            x='Age Group',
            y='Courses Taken',
            title='Average Courses Enrolled per Learner by Age Group',
            color='Age Group',
            color_discrete_sequence=COLOR_PALETTE,
            category_orders={"Age Group": ["Under 18", "18-25", "26-35"]}
        )
        fig_avg_age.update_layout(**PLOTLY_LAYOUT, yaxis_title="Avg Courses")
        st.plotly_chart(fig_avg_age, use_container_width=True)
        
    st.info(
        f"💡 **Behavioral Insight:** Active learners average **{user_counts['Courses Taken'].mean():.2f} courses**, "
        f"with the most active learner completing **{user_counts['Courses Taken'].max()} courses**. "
        f"The 18–25 age cohort exhibits the highest aggregate course velocity."
    )

# =========================================================================
# TAB 6: DATA EXPLORER
# =========================================================================
with tab6:
    st.subheader("📋 Dataset Explorer & Raw Data Representation")
    st.markdown("Inspect, search, and download the full relational datasets utilized in this analysis.")
    
    view_option = st.radio(
        "Select Dataset View:",
        ["Merged Analytics Records (6,800+ rows)", "Users Sheet (3,000 learners)", "Courses Catalog (50 courses)", "Transactions Log"],
        horizontal=True
    )
    
    if view_option == "Merged Analytics Records (6,800+ rows)":
        st.write(f"Showing **{len(filtered_df):,}** filtered records out of **{len(df):,}** total.")
        st.dataframe(
            filtered_df[['TransactionID', 'UserID', 'UserName', 'Age', 'Age Group', 'Gender', 'CourseID', 'CourseName', 'CourseCategory', 'CourseLevel', 'CourseType', 'TransactionDate']],
            use_container_width=True,
            height=400
        )
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Data as CSV", data=csv_data, file_name="edupro_filtered_data.csv", mime="text/csv")
        
    elif view_option == "Users Sheet (3,000 learners)":
        st.write(f"Full registered cohort: **{len(users_df):,} learners** (Ages 15–35).")
        st.dataframe(users_df, use_container_width=True, height=400)
        
    elif view_option == "Courses Catalog (50 courses)":
        st.write(f"Catalog: **{len(courses_df)} courses** across 8 categories.")
        st.dataframe(courses_df, use_container_width=True, height=400)
        
    else:
        st.write(f"Transactions Log: **{len(transactions_df):,} total enrollment events**.")
        st.dataframe(transactions_df, use_container_width=True, height=400)
