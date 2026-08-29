"""Student Grade Calculator."""

FILE_NAME = "student_grades.txt"
SEPARATOR = "=" * 60
CARD_SEPARATOR = "-" * 60


def show_section(title, symbol=""):
	"""Display a report-style section heading."""
	print(f"\n{SEPARATOR}")
	print(f"{symbol} {title}".strip())
	print(SEPARATOR)


class Student:
	"""Store a student's identifying information and calculated grade."""

	def __init__(self, name, student_id, test_scores):
		self.name = name
		self.id = student_id
		self.test_scores = test_scores
		self.average = sum(test_scores) / len(test_scores)
		self.grade = calculate_letter_grade(self.average)


def calculate_letter_grade(average):
	"""Return the letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def load_students():
	"""Load student records from the pipe-delimited data file."""
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					scores = [float(fields[index]) for index in range(2, 5)]
					students.append(Student(fields[0], fields[1], scores))
				except ValueError:
					print(f"Skipped invalid scores on line {line_number}.")
	except FileNotFoundError:
		return students
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students):
	"""Save all student records in the required pipe-delimited format."""
	show_section("SAVE RECORDS", "💾")
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				scores = "|".join(f"{score:.2f}" for score in student.test_scores)
				file.write(
					f"{student.name}|{student.id}|{scores}|"
					f"{student.average:.2f}|{student.grade}\n"
				)
		print(f"Saved {len(students)} student record(s).")
	except OSError as error:
		print(f"Could not save student records: {error}")


def get_score(test_number):
	"""Prompt until a valid score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Enter Test {test_number} score: "))
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 through 100.")
		except ValueError:
			print("Please enter a numeric score.")


def add_student(students):
	"""Prompt for and add one student record."""
	show_section("ADD NEW STUDENT")
	name = input("Enter student name: ").strip()
	student_id = input("Enter student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID are required.")
		return
	scores = [get_score(test_number) for test_number in range(1, 4)]
	student = Student(name, student_id, scores)
	students.append(student)
	print(f"\n✓ Added student: {student.name} (ID: {student.id})")
	print(f"  Average: {student.average:.2f} | Grade: {student.grade}")


def display_students(students):
	"""Display all student records in formatted report cards."""
	show_section("STUDENT RECORDS")
	if not students:
		print("No student records found.\n")
		return
	for student in students:
		print(CARD_SEPARATOR)
		print(student.name)
		print(f"Student ID: {student.id}\n")
		for test_number, score in enumerate(student.test_scores, start=1):
			print(f"Test {test_number} - {score:.2f}")
		print(f"\nAverage: {student.average:.2f}")
		print(f"Grade: {student.grade}")
		print(CARD_SEPARATOR + "\n")


def display_statistics(students):
	"""Display highest, lowest, and overall class averages."""
	show_section("CLASS STATISTICS", "📊")
	if not students:
		print("No student records available for statistics.\n")
		return
	averages = [student.average for student in students]
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	"""Find and display students whose names match the search text."""
	show_section("SEARCH STUDENTS", "🔍")
	search_name = input("Enter student name to search: ").strip().casefold()
	matches = [student for student in students if search_name in student.name.casefold()]
	if not matches:
		print("No matching students found.")
		return
	display_students(matches)


def show_menu():
	"""Display the main menu and return the user's selection."""
	show_section("STUDENT GRADE CALCULATOR")
	print("  1. Add new student")
	print("  2. Display student records")
	print("  3. Display class statistics")
	print("  4. Search students")
	print("  5. Exit and save records")
	print("\n  Press ESC to exit and save")
	return input("Choose an option: ").strip()


def main():
	"""Run the student grade calculator."""
	students = load_students()
	if students:
		print(f"\nLoaded {len(students)} student record(s).")
	else:
		print("\nNo existing student records found.")

	while True:
		choice = show_menu()
		if choice in ("5", "\x1b", "esc", "ESC"):
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		else:
			print("Invalid option. Please choose 1-5 or ESC.")


if __name__ == "__main__":
	main()
