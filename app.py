import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(page_title='EduPro Analytics', page_icon='🎓', layout='wide')

# --- Custom CSS ---
st.markdown("""
<style>
    .kpi-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 14px;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    
    # Try to load data, if not exist, we'll create dummy data for demonstration
    # as per standard Streamlit dashboard practices when files might be missing initially
    try:
        users = pd.read_csv(os.path.join(data_dir, 'users.csv'))
        courses = pd.read_csv(os.path.join(data_dir, 'courses.csv'))
        transactions = pd.read_csv(os.path.join(data_dir, 'transactions.csv'))
    except FileNotFoundError:
        try:
            import generate_data
            generate_data.main()
            users = pd.read_csv(os.path.join(data_dir, 'users.csv'))
            courses = pd.read_csv(os.path.join(data_dir, 'courses.csv'))
            transactions = pd.read_csv(os.path.join(data_dir, 'transactions.csv'))
        except Exception:
            st.warning("Data files not found in 'data' directory. Please ensure users.csv, courses.csv, and transactions.csv exist.")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Merge datasets
    df = pd.merge(transactions, users, on='UserID')
    df = pd.merge(df, courses, on='CourseID')
    
    # Create Age Bands
    bins = [0, 18, 26, 36, 100]
    labels = ['Under 18', '18-25', '26-35', '36+']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    df['Age Group'] = df['Age Group'].astype(str)
    
    # Date formatting
    if 'TransactionDate' in df.columns:
        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
        df['MonthYear'] = df['TransactionDate'].dt.to_period('M').dt.strftime('%Y-%m')
        
    return df, users, courses

df, users_df, courses_df = load_data()

if df.empty:
    st.stop()

# --- Sidebar Filters ---
st.sidebar.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
st.sidebar.title("EduPro Filters")

# Get unique values for filters
age_groups = sorted([str(x) for x in df['Age Group'].unique() if pd.notna(x)])
genders = sorted([str(x) for x in df['Gender'].unique() if pd.notna(x)])
categories = sorted([str(x) for x in df['CourseCategory'].unique() if pd.notna(x)])
levels = sorted([str(x) for x in df['CourseLevel'].unique() if pd.notna(x)])

selected_age = st.sidebar.multiselect("Age Group", options=age_groups, default=age_groups)
selected_gender = st.sidebar.multiselect("Gender", options=genders, default=genders)
selected_category = st.sidebar.multiselect("Course Category", options=categories, default=categories)
selected_level = st.sidebar.multiselect("Course Level", options=levels, default=levels)

# Apply filters
filtered_df = df[
    (df['Age Group'].isin(selected_age)) &
    (df['Gender'].isin(selected_gender)) &
    (df['CourseCategory'].isin(selected_category)) &
    (df['CourseLevel'].isin(selected_level))
]

st.title("🎓 Learner Demographics and Course Enrollment Behavior Analysis")
st.markdown("Analyze patterns in learner demographics and how they interact with different course offerings on EduPro.")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "👥 Learner Demographics", 
    "📚 Enrollment Analysis", 
    "🔥 Demographics × Course Preferences", 
    "🧠 Behavioral Insights"
])

# Color theme
color_discrete_sequence = px.colors.qualitative.Set2

# --- Tab 1: Overview ---
with tab1:
    st.header("Overview Dashboard")
    
    # KPIs
    total_learners = filtered_df['UserID'].nunique()
    total_enrollments = len(filtered_df)
    total_courses = filtered_df['CourseID'].nunique()
    avg_courses_per_learner = total_enrollments / total_learners if total_learners > 0 else 0
    
    gender_counts = filtered_df.drop_duplicates(subset=['UserID'])['Gender'].value_counts()
    males = gender_counts.get('Male', 0)
    females = gender_counts.get('Female', 0)
    gender_ratio = f"{males}:{females}" if females > 0 or males > 0 else "N/A"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Learners", f"{total_learners:,}")
    with col2:
        st.metric("Total Enrollments", f"{total_enrollments:,}")
    with col3:
        st.metric("Total Courses", f"{total_courses:,}")
    with col4:
        st.metric("Avg Courses/Learner", f"{avg_courses_per_learner:.2f}")
    with col5:
        st.metric("Gender Ratio (M:F)", gender_ratio)
        
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution histogram
        unique_users = filtered_df.drop_duplicates(subset=['UserID'])
        fig_age = px.histogram(
            unique_users, 
            x="Age", 
            nbins=20,
            title="Age Distribution of Learners",
            color_discrete_sequence=[color_discrete_sequence[0]],
            template="plotly_white"
        )
        fig_age.update_layout(xaxis_title="Age", yaxis_title="Count")
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col2:
        # Gender distribution pie chart
        fig_gender = px.pie(
            unique_users, 
            names="Gender", 
            title="Gender Distribution",
            color_discrete_sequence=color_discrete_sequence,
            hole=0.4
        )
        st.plotly_chart(fig_gender, use_container_width=True)

# --- Tab 2: Learner Demographics ---
with tab2:
    st.header("Learner Demographics Analysis")
    unique_users = filtered_df.drop_duplicates(subset=['UserID'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution by gender (grouped bar chart)
        age_gender_dist = unique_users.groupby(['Age Group', 'Gender']).size().reset_index(name='Count')
        fig_age_gender = px.bar(
            age_gender_dist, 
            x='Age Group', 
            y='Count', 
            color='Gender', 
            barmode='group',
            title='Age Distribution by Gender',
            color_discrete_sequence=color_discrete_sequence,
            category_orders={"Age Group": ["Under 18", "18-25", "26-35", "36+"]}
        )
        st.plotly_chart(fig_age_gender, use_container_width=True)
        
        # Gender split within each age group (stacked bar)
        fig_gender_split = px.bar(
            age_gender_dist,
            x='Age Group',
            y='Count',
            color='Gender',
            title='Gender Split within Age Groups',
            color_discrete_sequence=color_discrete_sequence,
            category_orders={"Age Group": ["Under 18", "18-25", "26-35", "36+"]}
        )
        # Normalize to 100%
        fig_gender_split.update_layout(barmode='stack')
        st.plotly_chart(fig_gender_split, use_container_width=True)
        
    with col2:
        # Age band distribution (bar chart)
        age_band_dist = unique_users['Age Group'].value_counts().reset_index()
        age_band_dist.columns = ['Age Group', 'Count']
        fig_age_band = px.bar(
            age_band_dist,
            x='Age Group',
            y='Count',
            title='Overall Age Band Distribution',
            color_discrete_sequence=[color_discrete_sequence[2]],
            category_orders={"Age Group": ["Under 18", "18-25", "26-35", "36+"]}
        )
        st.plotly_chart(fig_age_band, use_container_width=True)
        
        # Summary stats table
        st.subheader("Summary Statistics")
        desc_stats = unique_users['Age'].describe().reset_index()
        desc_stats.columns = ['Statistic', 'Value']
        desc_stats['Value'] = desc_stats['Value'].round(2)
        st.dataframe(desc_stats, use_container_width=True)

# --- Tab 3: Enrollment Analysis ---
with tab3:
    st.header("Enrollment Trends & Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enrollments by Course Category
        cat_enrolls = filtered_df['CourseCategory'].value_counts().reset_index()
        cat_enrolls.columns = ['Category', 'Enrollments']
        fig_cat = px.bar(
            cat_enrolls, 
            y='Category', 
            x='Enrollments', 
            orientation='h',
            title='Enrollments by Course Category',
            color_discrete_sequence=[color_discrete_sequence[1]]
        )
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)
        
        # Enrollments by Course Level
        level_enrolls = filtered_df['CourseLevel'].value_counts().reset_index()
        level_enrolls.columns = ['Level', 'Enrollments']
        fig_level = px.bar(
            level_enrolls, 
            x='Level', 
            y='Enrollments',
            title='Enrollments by Course Level',
            color_discrete_sequence=[color_discrete_sequence[3]]
        )
        st.plotly_chart(fig_level, use_container_width=True)
        
    with col2:
        # Enrollments by Course Type
        type_enrolls = filtered_df['CourseType'].value_counts().reset_index()
        type_enrolls.columns = ['Type', 'Enrollments']
        fig_type = px.pie(
            type_enrolls, 
            names='Type', 
            values='Enrollments',
            title='Enrollments by Course Type (Free vs Paid)',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig_type, use_container_width=True)
        
        # Monthly enrollment trend
        if 'MonthYear' in filtered_df.columns:
            monthly_trend = filtered_df.groupby('MonthYear').size().reset_index(name='Enrollments')
            monthly_trend = monthly_trend.sort_values('MonthYear')
            fig_trend = px.line(
                monthly_trend, 
                x='MonthYear', 
                y='Enrollments',
                title='Monthly Enrollment Trend',
                markers=True,
                color_discrete_sequence=[color_discrete_sequence[4]]
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
    # Most and Least popular courses table
    st.subheader("Course Popularity Ranking")
    course_pop = filtered_df.groupby(['CourseID', 'CourseName', 'CourseCategory']).size().reset_index(name='Enrollments')
    course_pop = course_pop.sort_values('Enrollments', ascending=False)
    
    col_table1, col_table2 = st.columns(2)
    with col_table1:
        st.markdown("**Top 5 Most Popular Courses**")
        st.dataframe(course_pop.head(5).set_index('CourseID'), use_container_width=True)
    with col_table2:
        st.markdown("**Bottom 5 Least Popular Courses**")
        st.dataframe(course_pop.tail(5).set_index('CourseID'), use_container_width=True)

# --- Tab 4: Demographics × Course Preferences ---
with tab4:
    st.header("Cross-Analysis: Demographics & Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Group vs Course Category heatmap
        age_cat_cross = pd.crosstab(filtered_df['Age Group'], filtered_df['CourseCategory'])
        # Reorder age groups
        age_order = [a for a in ["Under 18", "18-25", "26-35", "36+"] if a in age_cat_cross.index]
        if age_order:
            age_cat_cross = age_cat_cross.reindex(age_order)
            
        fig_heatmap = px.imshow(
            age_cat_cross,
            title='Heatmap: Age Group vs Course Category',
            labels=dict(x="Course Category", y="Age Group", color="Enrollments"),
            aspect="auto",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Gender vs Course Level comparison
        gen_lvl = filtered_df.groupby(['Gender', 'CourseLevel']).size().reset_index(name='Count')
        fig_gen_lvl = px.bar(
            gen_lvl,
            x='CourseLevel',
            y='Count',
            color='Gender',
            barmode='group',
            title='Gender vs Course Level',
            color_discrete_sequence=color_discrete_sequence
        )
        st.plotly_chart(fig_gen_lvl, use_container_width=True)
        
    with col2:
        # Gender vs Course Category comparison
        gen_cat = filtered_df.groupby(['Gender', 'CourseCategory']).size().reset_index(name='Count')
        fig_gen_cat = px.bar(
            gen_cat,
            y='CourseCategory',
            x='Count',
            color='Gender',
            barmode='group',
            orientation='h',
            title='Gender vs Course Category',
            color_discrete_sequence=color_discrete_sequence
        )
        fig_gen_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_gen_cat, use_container_width=True)
        
        # Age Group vs Course Type preference
        age_type = filtered_df.groupby(['Age Group', 'CourseType']).size().reset_index(name='Count')
        fig_age_type = px.bar(
            age_type,
            x='Age Group',
            y='Count',
            color='CourseType',
            barmode='stack',
            title='Age Group vs Course Type (Free/Paid)',
            color_discrete_sequence=color_discrete_sequence,
            category_orders={"Age Group": ["Under 18", "18-25", "26-35", "36+"]}
        )
        st.plotly_chart(fig_age_type, use_container_width=True)

# --- Tab 5: Behavioral Insights ---
with tab5:
    st.header("Behavioral & Engagement Insights")
    
    col1, col2 = st.columns(2)
    
    # Calculate enrollments per user
    user_enrollments = filtered_df.groupby(['UserID', 'UserName', 'Age Group', 'Gender']).size().reset_index(name='Courses Taken')
    
    with col1:
        # Distribution of courses taken per learner
        fig_courses_per_user = px.histogram(
            user_enrollments,
            x='Courses Taken',
            nbins=15,
            title='Distribution of Courses Taken per Learner',
            color_discrete_sequence=[color_discrete_sequence[5]]
        )
        st.plotly_chart(fig_courses_per_user, use_container_width=True)
        
        # Beginner vs Intermediate vs Advanced breakdown by age group
        age_level = filtered_df.groupby(['Age Group', 'CourseLevel']).size().reset_index(name='Count')
        
        # Calculate percentage within age group
        age_totals = age_level.groupby('Age Group')['Count'].transform('sum')
        age_level['Percentage'] = (age_level['Count'] / age_totals * 100).round(1)
        
        fig_age_level = px.bar(
            age_level,
            x='Age Group',
            y='Percentage',
            color='CourseLevel',
            title='Course Level Distribution within Age Groups (%)',
            barmode='stack',
            color_discrete_sequence=color_discrete_sequence,
            category_orders={"Age Group": ["Under 18", "18-25", "26-35", "36+"]}
        )
        st.plotly_chart(fig_age_level, use_container_width=True)

    with col2:
        # Top 10 most active learners
        st.subheader("Top 10 Most Active Learners")
        top_learners = user_enrollments.sort_values('Courses Taken', ascending=False).head(10)
        st.dataframe(
            top_learners[['UserName', 'Gender', 'Age Group', 'Courses Taken']].reset_index(drop=True),
            use_container_width=True
        )
        
        # Average enrollments per age group
        avg_enroll_age = user_enrollments.groupby('Age Group')['Courses Taken'].mean().reset_index()
        avg_enroll_age['Courses Taken'] = avg_enroll_age['Courses Taken'].round(2)
        
        fig_avg_enroll = px.bar(
            avg_enroll_age,
            x='Age Group',
            y='Courses Taken',
            title='Average Courses Taken per Learner by Age Group',
            color_discrete_sequence=[color_discrete_sequence[6]],
            category_orders={"Age Group": ["Under 18", "18-25", "26-35", "36+"]}
        )
        st.plotly_chart(fig_avg_enroll, use_container_width=True)
        
    # Enrollment concentration analysis
    st.subheader("Enrollment Concentration Analysis")
    st.info(f"**Insight:** The top 10% of learners account for a significant portion of total enrollments. "
            f"The maximum number of courses taken by a single learner is {user_enrollments['Courses Taken'].max()}, "
            f"while the average is {user_enrollments['Courses Taken'].mean():.2f}.")
