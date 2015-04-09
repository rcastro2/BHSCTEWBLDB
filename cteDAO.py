

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
        students_array = []
        students_in_form = form['students'].replace('\r','').split('\n')

        #Adjust students collection with students not in list
        old_students = self.get_wbl(title)
        if old_students != None:
            for old_student in old_students['students']:
                if old_student not in students_in_form:
                    self.students.update({'student_id':old_student[:9]},{'$pull':{"wbl":title}},True)

        #Adjust students collections with students in list
        for student in students_in_form:
            student_id = student[:9]
            if len(student_id) == 9:
                self.students.update({'student_id':student_id},{'$addToSet':{"wbl":title}},True)
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
            return self.students.find({'wbl':wbl}).sort('last',1)
        elif student == None:
            return self.students.find({}).sort('last',1)
        else:
            wbls = self.get_wbl()
            s = self.students.find_one({'student_id':student})
            s_wbls = []
            if 'wbl' in s:
                for wbl in s['wbl']:
                    for w in wbls:
                        if wbl == w['title']:
                            s_wbls.append({'title':wbl,'description':w['description'],'activity_date':w['activity_date']})
            data = {'student_id':s['student_id'],'last':s['last'],'first':s['first'],'wbl':s_wbls}
            return data
