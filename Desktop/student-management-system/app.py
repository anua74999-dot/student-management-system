import streamlit as st
import pandas as pd
from student import Student
from manager import StudentManager

# 1. Page Configuration
st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")

# 2. Inject Custom CSS for Student/Education Background
custom_bg = """
<style>
/* Main app background */
.stApp {
    background-image: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)), 
                      url("https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: rgba(240, 244, 248, 0.95) !important;
}

/* Content container styling for better readability */
.block-container {
    background: rgba(255, 255, 255, 0.85);
    padding: 2rem !important;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
    margin-top: 2rem;
}
</style>
"""
st.markdown(custom_bg, unsafe_allow_html=True)

# Rest of your app logic continues here...
manager = StudentManager()


# Initialize Application State
st.set_page_config(page_title="Student Management System", page_icon="🎓", layout="wide")
manager = StudentManager()

st.title("🎓 Student Management System")
st.markdown("---")

# Sidebar Menu Navigation
menu = ["View & Search", "Add Student", "Update Student", "Delete Student"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# ---------------- LIST & SEARCH ----------------
if choice == "View & Search":
    st.subheader("📋 Student Directory")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search by Name or ID", "")
    with col2:
        all_courses = ["All"] + list(set(s.course for s in manager.get_all_students() if s.course))
        selected_course = st.selectbox("🎯 Filter by Course", all_courses)

    filtered_list = manager.search_and_filter(search_query, selected_course)

    if filtered_list:
        data = [s.to_dict() for s in filtered_list]
        df = pd.DataFrame(data)
        df.columns = ["Student ID", "Full Name", "Age", "Grade", "Email", "Course"]
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No matching student records found.")

# ---------------- ADD STUDENT ----------------
elif choice == "Add Student":
    st.subheader("➕ Add New Student")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sid = st.text_input("Student ID (Unique)*")
            name = st.text_input("Full Name*")
            age = st.number_input("Age*", min_value=5, max_value=100, value=20)
        with col2:
            grade = st.selectbox("Grade*", ["A+", "A", "B+", "B", "C", "D", "F"])
            email = st.text_input("Email Address*")
            course = st.text_input("Course/Department*")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not sid or not name or not email or not course:
                st.error("Please fill in all mandatory fields.")
            else:
                new_student = Student(sid, name, age, grade, email, course)
                success, msg = manager.add_student(new_student)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

# ---------------- UPDATE STUDENT ----------------
elif choice == "Update Student":
    st.subheader("✏️ Update Student Record")
    students = manager.get_all_students()
    student_ids = [s.student_id for s in students]

    if not student_ids:
        st.info("No records available to update.")
    else:
        selected_id = st.selectbox("Select Student ID to Edit", student_ids)
        current_student = next(s for s in students if s.student_id == selected_id)

        with st.form("update_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", value=current_student.name)
                age = st.number_input("Age", min_value=5, max_value=100, value=current_student.age)
                grade = st.selectbox("Grade", ["A+", "A", "B+", "B", "C", "D", "F"], index=["A+", "A", "B+", "B", "C", "D", "F"].index(current_student.grade))
            with col2:
                email = st.text_input("Email", value=current_student.email)
                course = st.text_input("Course", value=current_student.course)
            
            update_btn = st.form_submit_button("Update Details")
            if update_btn:
                updated_data = {"name": name, "age": age, "grade": grade, "email": email, "course": course}
                success, msg = manager.update_student(selected_id, updated_data)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

# ---------------- DELETE STUDENT ----------------
elif choice == "Delete Student":
    st.subheader("🗑️ Delete Student Record")
    students = manager.get_all_students()
    student_ids = [s.student_id for s in students]

    if not student_ids:
        st.info("No records available to delete.")
    else:
        selected_id = st.selectbox("Select Student ID to Remove", student_ids)
        st.warning(f"Are you sure you want to permanently delete record for ID: **{selected_id}**?")
        
        if st.button("Confirm Delete"):
            success, msg = manager.delete_student(selected_id)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)