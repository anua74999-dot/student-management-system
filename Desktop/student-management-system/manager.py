from typing import List, Optional
from student import Student
from storage import DataStorage

class StudentManager:
    """Manages Student operations (CRUD, Search, Filter) with exception handling."""
    def __init__(self):
        self.storage = DataStorage()
        self.students: List[Student] = [
            Student.from_dict(d) for d in self.storage.load_students()
        ]

    def _save(self):
        self.storage.save_students([s.to_dict() for s in self.students])

    def add_student(self, student: Student) -> tuple[bool, str]:
        """Adds a new student record."""
        try:
            if any(s.student_id == student.student_id for s in self.students):
                return False, f"Student ID '{student.student_id}' already exists!"
            self.students.append(student)
            self._save()
            return True, "Student added successfully!"
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def get_all_students(self) -> List[Student]:
        """Returns all students."""
        return self.students

    def update_student(self, student_id: str, updated_data: dict) -> tuple[bool, str]:
        """Updates an existing student's details."""
        try:
            for s in self.students:
                if s.student_id == student_id:
                    s.name = updated_data.get("name", s.name)
                    s.age = updated_data.get("age", s.age)
                    s.grade = updated_data.get("grade", s.grade)
                    s.email = updated_data.get("email", s.email)
                    s.course = updated_data.get("course", s.course)
                    self._save()
                    return True, "Student updated successfully!"
            return False, "Student ID not found."
        except Exception as e:
            return False, f"Update failed: {str(e)}"

    def delete_student(self, student_id: str) -> tuple[bool, str]:
        """Deletes a student record by ID."""
        try:
            initial_count = len(self.students)
            self.students = [s for s in self.students if s.student_id != student_id]
            if len(self.students) < initial_count:
                self._save()
                return True, "Student record deleted successfully!"
            return False, "Student ID not found."
        except Exception as e:
            return False, f"Deletion failed: {str(e)}"

    def search_and_filter(self, query: str = "", course_filter: str = "All") -> List[Student]:
        """Searches by ID/Name and filters by Course."""
        results = self.students

        if query:
            q = query.lower().strip()
            results = [s for s in results if q in s.name.lower() or q in s.student_id.lower()]

        if course_filter != "All":
            results = [s for s in results if s.course.lower() == course_filter.lower()]

        return results