import slate
import re
import numpy as np

# Assumptions: Precisely one student per page. No +'s or -'s in grades.

def GPA_from_letter_grades(letterGrades):
    """
    Computes a floating point GPA for a student given a list of their letter grades.
    """
    letter2number = {'A':4.0, 'B':3.0, 'C':2.0, 'D':1.0, 'F':0.0}
    return np.mean([letter2number[letter] for letter in letterGrades if letter != '0'])

# First, find the file.

# Then, extract text from the file.
with open('streamPDF.pdf', 'rb') as f:
    raw = slate.PDF(f)

# Parse the text.
students = []
for page in raw:
    # First find the name of the student.
    name = re.search(r"Progress Report For (.*) \(", page).group(1)
    # Then grab the section containing their grades.
    # The section contraining the grades begins with "Overall".
    gradeSection = re.search(r"Overall(.*?)Date", page, re.S).group(1)
    # Break that section into classes.
    # Each class ends with a number of missing assignments; split on that.
    classChunks = re.split(r"\n[\d]+\n", gradeSection)[:-1] # Last one is empty.
    # Now extract their overall grade for each class.
    letterGrades = []
    for chunk in classChunks:
        try:
            letterGrades.append(re.search(r"(\w)\n\n", chunk).group(1))
        except:
            # Only known exception is no grades in yet; just ignore for GPA.
            pass

    students.append({'name': name,
                     'letterGrades' : letterGrades,
                     'GPA' : GPA_from_letter_grades(letterGrades)})

# Display results.
output = ""
for student in sorted(students, key=lambda x: -x['GPA']):
    output += student['name'] + ': ' + '{:.2f}'.format(student['GPA']) + '\n'
output += "Class Average GPA: " + str(np.mean([student['GPA'] for student in students]))

print output
