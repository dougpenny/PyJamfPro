#
# dict_to_xml.py
#
# Copyright (c) 2022 Doug Penny
# Licensed under MIT
#
# See LICENSE.md for license information
#
# SPDX-License-Identifier: MIT
#

from typing import Dict
from xml.etree import ElementTree


def class_dict_to_xml(class_dict: Dict) -> bytes:
    """
        Converts a dictionary of class data into
        the required XML for sending to Jamf.

        Args:
            class_dict (Dict): Dictionary representation
            of the class information

        Returns:
            A byte string representing of the XML class information.
        """
    jamf_class = ElementTree.Element('class')
    name = ElementTree.SubElement(jamf_class, 'name')
    name.text = class_dict.get('name')
    description = ElementTree.SubElement(jamf_class, 'description')
    description.text = class_dict.get('description')
    type = ElementTree.SubElement(jamf_class, 'type')
    type.text = 'Usernames'
    students = ElementTree.SubElement(jamf_class, 'students')
    for student in class_dict.get('students'):
        class_student = ElementTree.SubElement(students, 'student')
        class_student.text = student
    teachers = ElementTree.SubElement(jamf_class, 'teachers')
    for teacher in class_dict.get('teachers'):
        class_teacher = ElementTree.SubElement(teachers, 'teacher')
        class_teacher.text = teacher
    return ElementTree.tostring(jamf_class)
