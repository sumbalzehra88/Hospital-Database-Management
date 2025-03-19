import streamlit as st
import hashlib
import sqlite3
from datetime import datetime
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for enhanced UI with blue and sea green theme
st.markdown("""
<style>
    /* General Styles */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f8ff;
        color: #333;
    }
    .main-header {
        font-size: 2.5rem;
        color: #0066cc;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .subheader {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s, box-shadow 0.3s;
        border-top: 4px solid #2E8B57;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 16px rgba(0, 0, 0, 0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #2E8B57 0%, #3a9ecb 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .metric-delta {
        font-size: 0.9rem;
        padding: 3px 8px;
        border-radius: 10px;
        background-color: rgba(255,255,255,0.2);
        display: inline-block;
        margin-top: 5px;
    }
    .info-box {
        background-color: #e6f7ff;
        border-left: 5px solid #0099ff;
        padding: 12px 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    .success-box {
        background-color: #e6ffee;
        border-left: 5px solid #2E8B57;
        padding: 12px 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    .warning-box {
        background-color: #fff8e1;
        border-left: 5px solid #FFC107;
        padding: 12px 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    .stButton button {
        background: linear-gradient(to right, #0066cc, #2E8B57);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background: linear-gradient(to right, #005cb8, #267349);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .logout-btn button {
        background: linear-gradient(to right, #e53935, #d32f2f);
        color: white;
    }
    .logout-btn button:hover {
        background: linear-gradient(to right, #c62828, #b71c1c);
    }
    .welcome-text {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0066cc;
        text-shadow: 1px 1px 1px rgba(0,0,0,0.05);
    }
    .sidebar-content {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 8px;
    }
    /* Activity Styles */
    .activity-item {
        background-color: #f0f8ff;
        border-left: 4px solid #2E8B57;
        padding: 12px 15px;
        margin-bottom: 10px;
        border-radius: 4px;
        transition: transform 0.2s;
    }
    .activity-item:hover {
        transform: translateX(5px);
        background-color: #e6f7ff;
    }
    .activity-time {
        font-size: 0.8rem;
        color: #0066cc;
        font-weight: bold;
    }
    .activity-text {
        margin-top: 5px;
    }
    /* Navigation Styles */
    .navigation-item {
        padding: 10px 15px;
        margin: 5px 0;
        background-color: rgba(46, 139, 87, 0.1);
        border-radius: 8px;
        transition: all 0.3s;
    }
    .navigation-item:hover, .navigation-item.active {
        background-color: rgba(46, 139, 87, 0.2);
        transform: translateX(5px);
    }
    /* Chart Placeholder */
    .chart-container {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 15px;
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-style: italic;
        color: #0066cc;
        border: 1px dashed #2E8B57;
    }
    /* Dark Mode */
    .dark-mode {
        background-color: #0a192f;
        color: #ffffff;
    }
    .dark-mode .card {
        background-color: #1a2c4e;
        color: #ffffff;
        border-top: 4px solid #3a9ecb;
    }
    .dark-mode .stButton button {
        background: linear-gradient(to right, #3a9ecb, #2E8B57);
    }
    .dark-mode .stButton button:hover {
        background: linear-gradient(to right, #3182b0, #267349);
    }
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    /* Dashboard Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }
    .stat-card {
        background: linear-gradient(135deg, #0066cc 0%, #2E8B57 100%);
        color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Connect to the hospital.db database
def get_db_connection():
    return sqlite3.connect("hospital.db", check_same_thread=False)

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password against stored hash
def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password

# Register new user in the database
def register_newuser(username, password, email, user_type):
    if not username or not email or not password:
        st.markdown('<div class="warning-box">All fields are required.</div>', unsafe_allow_html=True)
        return

    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO USER_DATA (username, password, email, user_type) VALUES (?, ?, ?, ?)", 
                      (username, hash_password(password), email, user_type))
            conn.commit()
            st.markdown('<div class="success-box">User registered successfully! Please log in.</div>', unsafe_allow_html=True)
        except sqlite3.IntegrityError:
            st.markdown('<div class="warning-box">Username already exists. Try a different one.</div>', unsafe_allow_html=True)

# Authenticate login credentials
def login(username, password):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT password, user_type FROM USER_DATA WHERE username = ?", (username,))
        result = c.fetchone()
        
    if result is not None and verify_password(password, result[0]):
        return True, result[1]  # Return True and user_type
    return False, None

# User Authentication Page
def user_authentication_page():
    st.markdown('<h1 class="main-header">User Authentication</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2 class="subheader">Login</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            col_btn1, col_btn2 = st.columns([1, 2])
            with col_btn1:
                submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                success, user_type = login(username, password)
                if success:
                    st.session_state.update({
                        "logged_in": True, 
                        "username": username,
                        "user_type": user_type
                    })
                    st.markdown('<div class="success-box">Login successful!</div>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<div class="warning-box">Invalid credentials. Please try again.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<h2 class="subheader">Register</h2>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password", placeholder="Create a password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            user_type = st.selectbox("User Type", ("Patient", "Admin", "Doctor", "Nurse", "Cashier"))
            col_btn1, col_btn2 = st.columns([1, 2])
            with col_btn1:
                submitted = st.form_submit_button("Sign Up", use_container_width=True)

            if submitted:
                if password != confirm_password:
                    st.markdown('<div class="warning-box">Passwords do not match.</div>', unsafe_allow_html=True)
                else:
                    register_newuser(username, password, email, user_type)
        st.markdown('</div>', unsafe_allow_html=True)

admin_df = pd.read_csv("Admin.csv")
staff_df = pd.read_csv("Staff_table_filled.csv")

def register_newuser(username, password, email, user_type):
    if not username or not email or not password:
        st.markdown('<div class="warning-box">All fields are required.</div>', unsafe_allow_html=True)
        return

    # If user is not a Patient, check if they exist in Admin or Staff table
    if user_type != "Patient":
        in_admins = username.lower() in admin_df["Name"].str.lower().values
        in_staff = username.lower() in staff_df["NAME"].str.lower().values

        if not (in_admins or in_staff):
            st.markdown(f'<div class="warning-box">{user_type}s must already exist in the system. Contact Admin.</div>', unsafe_allow_html=True)
            return

    # Connect to database and insert user
    with get_db_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO USER_DATA (username, password, email, user_type) VALUES (?, ?, ?, ?)", 
                      (username, hash_password(password), email, user_type))
            conn.commit()
            st.markdown('<div class="success-box">User registered successfully! Please log in.</div>', unsafe_allow_html=True)
        except sqlite3.IntegrityError:
            st.markdown('<div class="warning-box">Username already exists. Try a different one.</div>', unsafe_allow_html=True)

# Enhanced Dashboard components
def show_dashboard(user_type):
    st.markdown('<h2 class="subheader">Dashboard</h2>', unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown(f"""
    <div class="card fade-in" style="background: linear-gradient(135deg, #e6f7ff 0%, #e6ffee 100%);">
        <h3>Welcome back, {st.session_state["username"]}!</h3>
        <p>Today is {datetime.now().strftime("%A, %B %d, %Y")}. Here's your daily overview.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display enhanced metrics based on user type with animation delay
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card fade-in" style="animation-delay: 0.1s; background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);">
            <div class="metric-label">Today's Appointments</div>
            <div class="metric-value">5</div>
            <div class="metric-delta">↑ 2 from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card fade-in" style="animation-delay: 0.2s; background: linear-gradient(135deg, #2E8B57 0%, #3cb371 100%);">
            <div class="metric-label">Pending Reports</div>
            <div class="metric-value">3</div>
            <div class="metric-delta">↓ 1 from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card fade-in" style="animation-delay: 0.3s; background: linear-gradient(135deg, #1a75ff 0%, #00b3b3 100%);">
            <div class="metric-label">Tasks Completed</div>
            <div class="metric-value">12</div>
            <div class="metric-delta">↑ 3 from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card fade-in" style="animation-delay: 0.4s; background: linear-gradient(135deg, #007399 0%, #2E8B57 100%);">
            <div class="metric-label">Patient Satisfaction</div>
            <div class="metric-value">95%</div>
            <div class="metric-delta">↑ 2% this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Two column layout for charts and activity
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<h3>Analytics Overview</h3>', unsafe_allow_html=True)
        
        # Tabs for different charts
        tab1, tab2, tab3 = st.tabs(["Patient Flow", "Department Stats", "Resource Utilization"])
        
        with tab1:
            st.markdown("""
            <div class="chart-container">
                [Patient Flow Chart Visualization]
                <br>Shows hourly patient admission and discharge rates
            </div>
            """, unsafe_allow_html=True)
            
        with tab2:
            st.markdown("""
            <div class="chart-container">
                [Department Performance Chart]
                <br>Compares key metrics across hospital departments
            </div>
            """, unsafe_allow_html=True)
            
        with tab3:
            st.markdown("""
            <div class="chart-container">
                [Resource Utilization Chart]
                <br>Tracks bed occupancy and equipment usage
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick action buttons
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<h3>Quick Actions</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("Schedule Appointment", use_container_width=True)
        with col2:
            st.button("Patient Lookup", use_container_width=True)
        with col3:
            st.button("Create Report", use_container_width=True)
        with col4:
            st.button("System Settings", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # Recent activity
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<h3>Recent Activity</h3>', unsafe_allow_html=True)
        
        # Sample activities based on user type
        activities = {
            "Patient": [
                {"time": "10:30 AM", "text": "Appointment scheduled with Dr. Smith for March 20, 2025"},
                {"time": "Yesterday", "text": "Medical report uploaded"},
                {"time": "Mar 10", "text": "Payment completed for prescription"}
            ],
            "Doctor": [
                {"time": "1 hour ago", "text": "Patient consultation with John Doe"},
                {"time": "3 hours ago", "text": "Lab results received for patient #12345"},
                {"time": "Yesterday", "text": "Treatment plan updated for patient #54321"}
            ],
            "Admin": [
                {"time": "2 hours ago", "text": "New doctor onboarded: Dr. Johnson"},
                {"time": "Yesterday", "text": "System maintenance scheduled for March 25"},
                {"time": "Mar 15", "text": "Monthly patient statistics generated"}
            ],
            "Nurse": [
                {"time": "30 mins ago", "text": "Medication administered to room 302"},
                {"time": "2 hours ago", "text": "Vital signs recorded for patient #67890"},
                {"time": "Yesterday", "text": "Shift handover completed"}
            ],
            "Cashier": [
                {"time": "1 hour ago", "text": "Payment received from patient #12345"},
                {"time": "3 hours ago", "text": "Insurance claim submitted for patient #54321"},
                {"time": "Yesterday", "text": "Monthly billing report generated"}
            ]
        }
        
        default_activities = [
            {"time": datetime.now().strftime("%H:%M"), "text": "Login detected"},
            {"time": "Today", "text": "System accessed"},
            {"time": "Today", "text": "Welcome to Hospital Management System"}
        ]
        
        for activity in activities.get(user_type, default_activities):
            st.markdown(f"""
            <div class="activity-item">
                <div class="activity-time">{activity['time']}</div>
                <div class="activity-text">{activity['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Upcoming events
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<h3>Upcoming Events</h3>', unsafe_allow_html=True)
        
        events = [
            {"date": "Mar 20", "text": "Staff Meeting"},
            {"date": "Mar 22", "text": "System Update"},
            {"date": "Mar 25", "text": "Training Session"}
        ]
        
        for event in events:
            st.markdown(f"""
            <div class="activity-item" style="border-left-color: #0066cc;">
                <div class="activity-time">{event['date']}</div>
                <div class="activity-text">{event['text']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# Main Application of Hospital Management System
def main():
    # Initialize session state variables if not exist
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_type" not in st.session_state:
        st.session_state["user_type"] = None

    # Main header
    with st.container():
        cols = st.columns([1, 3, 1])
        with cols[1]:
            st.markdown('<h1 class="main-header">🏥 Hospital Management System</h1>', unsafe_allow_html=True)
    
    # Sidebar with navigation
    with st.sidebar:
        st.image("https://api.placeholder.com/200/100?text=Hospital+Logo", width=200)
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        if st.session_state["logged_in"]:
            st.markdown(f'<p class="welcome-text">Welcome, {st.session_state["username"]} ({st.session_state["user_type"]})</p>', unsafe_allow_html=True)
            
            # Navigation options based on user type
            if st.session_state["user_type"] == "Admin":
                page = st.radio("Navigation", ["Dashboard", "Appointments", "Medical Records", "Billing", "Users", "Settings"])
            elif st.session_state["user_type"] == "Doctor":
                page = st.radio("Navigation", ["Dashboard", "Appointments", "Medical Records", "Patients"])
            elif st.session_state["user_type"] == "Patient":
                page = st.radio("Navigation", ["Dashboard", "Appointments", "Medical Records", "Billing"])
            elif st.session_state["user_type"] == "Nurse":
                page = st.radio("Navigation", ["Dashboard", "Appointments", "Patient Care", "Medication"])
            elif st.session_state["user_type"] == "Cashier":
                page = st.radio("Navigation", ["Dashboard", "Billing", "Payments", "Reports"])
            else:
                page = st.radio("Navigation", ["Dashboard", "Appointments", "Medical Records", "Billing"])
            
            st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
            if st.button("Logout", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["user_type"] = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            page = st.radio("Navigation", ["User Authentication", "About", "Contact Us"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-box">Need help? Contact IT support at support@hospital.com</div>', unsafe_allow_html=True)
    
    # Main content area
    if st.session_state["logged_in"]:
        if page == "Dashboard":
            show_dashboard(st.session_state["user_type"])
        else:
            st.info(f"The {page} page is under construction.")
    else:
        if page == "User Authentication":
            user_authentication_page()
        elif page == "About":
            st.markdown('<h2 class="subheader">About Us</h2>', unsafe_allow_html=True)
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown("""
            ### Welcome to Our Hospital Management System
            
            Our Hospital Management System is designed to streamline healthcare operations and improve patient care through efficient digital management of hospital resources, appointments, and records.
            
            **Key Features:**
            - Patient record management
            - Appointment scheduling
            - Billing and payment processing
            - Staff management
            - Report generation
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        elif page == "Contact Us":
            st.markdown('<h2 class="subheader">Contact Us</h2>', unsafe_allow_html=True)
            st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
            st.markdown("""
            ### Get in Touch
            
            **Email:** support@hospital.com  
            **Phone:** (555) 123-4567  
            **Address:** 123 Medical Center Blvd, Healthcare City
            
            **Hours of Operation:**  
            Monday - Friday: 8:00 AM - 6:00 PM  
            Saturday: 9:00 AM - 1:00 PM  
            Sunday: Closed
            """)
            
            with st.form("contact_form"):
                name = st.text_input("Your Name")
                email = st.text_input("Your Email")
                message = st.text_area("Message")
                submitted = st.form_submit_button("Send Message")
                
                if submitted:
                    st.success("Message sent! We'll get back to you soon.")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()