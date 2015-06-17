import os, sys, pymongo, csv

#con = pymongo.MongoClient(os.environ.get('DATABASE_URL'))
con = pymongo.MongoClient("mongodb://localhost")
db = con.bhsbox

count = 0
if len(sys.argv) == 2:
    with open(sys.argv[1],'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count += 1
            s = {'$set':{'first':row["FirstName"],'last':row["LastName"],'gender':row["Gender"],'ethnic':row["EthnicCode"],'ofcl':row["OffClass"]}}
            db.students.update({'student_id':row["StudentID"]},s,True)
            print count, row["LastName"]
