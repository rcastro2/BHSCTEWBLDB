

import sys
import datetime
import pprint
class cteDAO:

    def __init__(self, database):
        self.students = database.students
        self.wbl = database.wbl

    def get_wbl(self,title=None):
        if title == None:
            return self.wbl.find({}).sort('activity_date',-1)
        else:
            return self.wbl.find_one({'title':title})

    def remove_wbl(self,title):
        return self.wbl.remove({'title':title})

    def upsert_wbl(self, form):
        title = form['title']
    	activity_date = form['activity_date']
        location = form['location']
        description = form['description']
        students_in_form = form['students'].replace('\r','').split('\n')
        students_in_DB = []
        students_not_in_DB = []

        #Adjust students collections with students in list
        for student in students_in_form:
            student_id = student[:9]
            s = self.students.find_one({'student_id':student_id})
            if s != None:
                students_in_DB.append({'student_id':s['student_id'],'last':s['last'],'first':s['first']})
            else:
                students_not_in_DB.append(student)

        activity = {"title": title,
                "activity_date": activity_date,
                "location": location,
                "description":description,
                "students": students_in_DB,
                "date": datetime.datetime.utcnow()}

        try:
            self.wbl.update({'title':title},activity,True)
        except:
            print "Error inserting post"
            print "Unexpected error:", sys.exc_info()[0]

        return True

    def get_students(self,student=None,wbl=None):
        if wbl != None:
            return self.wbl.find_one({'title':wbl})
        elif student == None:
            return self.students.find({}).sort('last',1)
        elif student != None:
            return self.wbl.find({'students.student_id':student}).sort('activity_date',-1)
        else:
            return False
