import unittest
import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Rashmi_Khurana import file_reading_gen


class Student:

    PT_Fields = ['CWID', 'NAME', 'MAJOR', 'COURSE']

    def __init__(self, stdcwid, name, major):
        """Update Student info"""
        self._cwid = stdcwid
        self._name = name
        self._major = major

        self._course = dict()

    def add_course(self, course, grade):
        """Updates Student Course and Grades"""
        self._course[course] = grade

    def pt_row(self):
        """Student Pretty table"""
        return self._cwid, self._name, self._major, sorted(self._course.keys())


class Instructors:

    PT_Fields = ['CWID', 'NAME', 'DEPT', 'COURSE', 'STUDENTS']

    def __init__(self, cwid, name, dept):
        """Update instructor info"""
        self._cwid = cwid
        self._name = name
        self._dept = dept

        self._course = defaultdict(int)

    def add_course(self, course):
        """Updates Student Course and Grades"""
        self._course[course] += 1

    def pt_row(self):
        """Instructor's Pretty Table"""
        ls = []
        for course, student in self._course.items():
            ls.append([self._cwid, self._name, self._dept, course, student])
        return ls


class Repository:
    """Class to call other classes"""
    def __init__(self, dir_path, pt=False, test=False):
        self._students = dict()
        self._instructors = dict()

        try:
            self._get_students(os.path.join(dir_path, "students.txt"))
            self._get_instructors(os.path.join(dir_path, "instructors.txt"))
            self._get_grades(os.path.join(dir_path, "grades.txt"))
        except FileNotFoundError as fnfe:
            print(fnfe)

        if pt:
            self.student_PT()
            self.instructor_PT()

        if test:
            self.student_test()
            self.instructor_test()

    def _get_students(self, path):
        try:
            for stdcwid, name, major in file_reading_gen(path, fields=3, sep='\t', header=False):
                if stdcwid in self._students:
                    raise ValueError(f"Duplicate CWID:{stdcwid}")
                else :
                    self._students[stdcwid] = Student(stdcwid, name, major)
        except FileNotFoundError as fnfe:
            print(fnfe)

    def _get_instructors(self, path):
        try:
            for instrcwid, name, dept in file_reading_gen(path, fields=3, sep='\t', header=False):
                if instrcwid in self._instructors:
                    raise ValueError(f"Duplicate CWID:{instrcwid}")
                else :
                    self._instructors[instrcwid] = Instructors(instrcwid, name, dept)
        except FileNotFoundError as fnfe:
            print(fnfe)

    def _get_grades(self, path):
        """get grades/no. of student and add then to Student/Instructors class"""
        try:
            for stdcwid, course, grade, instrcwid in file_reading_gen(path, fields=4, sep='\t', header=False):
                if stdcwid in self._students:
                    self._students[stdcwid].add_course(course, grade)
                else:
                    print(f"Student {stdcwid} not present")

                if instrcwid in self._instructors:
                    self._instructors[instrcwid].add_course(course)
                else:
                    print(f"Unknown Instructor {instrcwid}")
        except FileNotFoundError as fnfe:
            print(fnfe)

    def student_PT(self):
        """Print Student table"""
        pt = PrettyTable(Student.PT_Fields)
        for cwid in self._students.keys():
            pt.add_row(self._students[cwid].pt_row())
        print(pt)

    def instructor_PT(self):
        """Print Instructor table"""
        pt = PrettyTable(Instructors.PT_Fields)
        for instr in self._instructors.keys():
            for value in self._instructors[instr].pt_row():
                pt.add_row(value)
        print(pt)

    def student_test(self):
        st = []
        for cwid in self._students.keys() :
            st.append(self._students[cwid].pt_row())
        print(st)
        return st

    def instructor_test(self):
        it = []
        for instr in self._instructors.keys():
            for value in self._instructors[instr].pt_row():
                it.append(value)
        print(it)
        return it


def main():
    stevens = Repository('C:/Users/Rashmi/PycharmProjects/ssw810', pt=True, test=True)
    return stevens


class TestModule(unittest.TestCase):
    """Test File"""
    def test_hw09(self):
        """Manual Testing"""
        #Blank grade for new students
        #Error message for Duplicate CWID for student and instructor
        #Error message for Wrong directory address
        obj = Repository('C:/Users/Rashmi/PycharmProjects/ssw810', test=True)
        self.assertEqual(obj.student_test(), [('10103', 'Baldwin, C', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'])])
        self.assertEqual(obj.instructor_test(),[['98765', 'Einstein, A', 'SFEN', 'SSW 567', 1], ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 1], ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 1]])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
