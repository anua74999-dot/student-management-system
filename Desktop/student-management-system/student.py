class Student:
    """Represents a Student entity using OOP concepts."""
    def __init__(self, student_id: str, name: str, age: int, grade: str, email: str, course: str):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email
        self.course = course

    def to_dict(self) -> dict:
        """Converts object attributes to a dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "email": self.email,
            "course": self.course
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Student instance from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            grade=data["grade"],
            email=data["email"],
            course=data["course"]
        )