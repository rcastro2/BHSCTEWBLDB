

import sys
import re
import datetime

class cteDAO:

    def __init__(self, database):
        self.db = database
        self.students = database.students
        self.wbl = database.wbl

    def get_wbl(self,title=None):
        if title == None:
            return self.wbl.find({})
        else:
            return self.wbl.find({'title':title})

    def remove_wbl(self,title):
        return self.wbl.remove({'title':title})

    def upsert_wbl(self, form):
        title = form['title']
    	activity_date = form['activity_date']
        location = form['location']
        description = form['description']
        students_array = []
        for student in form['students'].replace('\r','').split('\n'):
            self.students.update({'student_id':student},{'$addToSet':{"wbl":title}},True)
            students_array.append(student)

        activity = {"title": title,
                "activity_date": activity_date,
                "location": location,
                "description":description,
                "students": students_array,
                "date": datetime.datetime.utcnow()}

        try:
            self.wbl.update({'title':title},activity,True)
        except:
            print "Error inserting post"
            print "Unexpected error:", sys.exc_info()[0]

        return True

    def get_students(self,student=None,wbl=None):
        if wbl != None:
            return self.students.find({'wbl':wbl})
        elif student == None:
            return self.students.find({})
        else:
            return self.students.find({'student_id':student})
