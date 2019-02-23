import os
import csv
from datetime import datetime

from IL_release import Ill_Member
from FED_release import *

import_path = os.path.join(".","import","memblist021719.csv")

list = []
with open(import_path,'r') as imp_file:
    imp_reader = csv.reader(imp_file, delimiter=' ', quotechar='|')
    for row in imp_reader:
        list+=row




timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
export_path = os.path.join(".","export","ReleaseLookup%s.csv" % timestamp )

# list = ['Y24350']
counter = 0
total = len(list)
with open(export_path, 'w') as exp_file:
    filewriter = csv.writer(exp_file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['id', 'Legal Name', 'Prison', 'Release Date', 'Parole Date', 'Life', 'Registry', 'MSR'])
    for raw_id in list:
        counter += 1
        print raw_id , "\t%s out of %s" % (counter, total)
        try:
            id = ''.join(e for e in raw_id if e.isalnum())
            if id.isdigit():
                id = id.zfill(8)
                memb = Fed_Member(id).get_csv_list()
            else:
                memb = Ill_Member(id).get_csv_list()
            filewriter.writerow(memb)
        except Exception as inst:
            filewriter.writerow([raw_id, inst])


