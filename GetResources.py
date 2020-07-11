
import time
import random
import glob
import os
import json
import shutil, errno
import fileinput

# base='G:\\Projects\\DataViz-Lesson-Plans\\01-Lesson-Plans\\05-Matplotlib\\3\\Activities\\02-Ins_Quartiles_and_Outliers\\Resources\\lax_temperature.csv'



# print(root_logDir)
def createResources(weekNo, dayNo, baseName, pathToYourLessonPlans,pathOut):
    def create_base_for_results(base):
        '''This moves the merged file to log folder created for it'''
        # path to root log directory 
        root_logDir = pathOut
        resource_dir=os.path.join(root_logDir,'Resources')
        # print(resource_dir)
        def move_file_sub_log_dir(base):
            '''This moves the baseFile to sub log directory'''
            # generate run id based on current time

            
            # path to move baseFile
            move_to_path = resource_dir
            if not os.path.isdir(move_to_path):
                os.makedirs(move_to_path)
            base_file = base

            # path to move Resources
            # res_move_to_path =os.path.join(move_to_path,'Resources')
            if not os.path.isdir(resource_dir):
                os.makedirs(resource_dir)

            # finally move baseFile
            import shutil
            # print(base_file,' ',move_to_path)
            shutil.copy(base_file, resource_dir)
            print(f"\n## Access merged file at the following location ##\n{resource_dir}")
        
        move_file_sub_log_dir(base)





    for x in os.walk(pathToYourLessonPlans):
        for pyout in glob.glob(x[0]+"\\"+weekNo+"*\\"+dayNo+"\\Activities\\*Ins*\\Resources\\*", recursive=True):
                # print(pyout)
                
                create_base_for_results(pyout)

# createResources(weekNo,dayNo,baseName,pathToYourLessonPlans,'05_merged')