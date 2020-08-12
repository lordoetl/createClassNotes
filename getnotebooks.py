
  
###############
# This is the driver that will grab all of your notebooks out of the instructor activites and merge them
# This will also grab the Resources and put them in a single folder.
#
# The jupyter merging part of this was duplicated from:
# '''
# # Author: Sunny Bhaveen Chandra
# # Contact: sunny.c17hawke@gmail.com
# '''
#
#
#  INSTRUCTIONS:
#  change the following variables and run
#  pathToYourLessonPlans=<this is the path to where you have cloned your lessonplans>
#  weekNo="<the week you are in>"
#  dayNo="<which of the 3 days you are in>"
#
#  You can change baseName if you want to change the name of the file.
###
import time
import random
import glob
import os
import json
import time
import GetResources

weekNo="10"
dayNo="2"
baseName = weekNo+'_Notes.ipynb'
pathToYourLessonPlans='G:\\Projects\\DataViz-Lesson-Plans\\01-Lesson-Plans\\'

def createListOFiles(weekNo,day):
    thisdir = pathToYourLessonPlans
    extensions=['.ipynb']
    files=[]
    for x in os.walk(thisdir):
       
        for ext in extensions:
             for py in glob.glob(x[0]+"\\"+weekNo+"*\\"+day+"\\Activities\\*Ins*\\Solved\\*"+ext, recursive=True):
                # print(py)
                if len(py)>0:
                    files.append(py)
    return files



def create_baseFile(baseName):
	'''This creates a base file in which we merge all the files'''
	baseData = '''{
	"cells": [{"cell_type": "markdown", "metadata": {},
	"source": ["# *Merged Jupyter Notebook*"]}],
	"metadata": {
	"kernelspec": {
	"display_name": "Python 3",
	"language": "python",
	"name": "python3"},
	"language_info": {
	"codemirror_mode": {"name": "ipython","version": 3},
	"file_extension": ".py",
	"mimetype": "text/x-python",
	"name": "python",
	"nbconvert_exporter": "python",
	"pygments_lexer": "ipython3",
	"version": "3.7.4"}
	},
	
	"nbformat": 4,
	"nbformat_minor": 2}'''

	Filename = baseName
	with open(Filename,'w+') as f:
	    f.write(baseData)

def read_file_as_json(Filename):
    with open(Filename,'r', errors='ignore') as f:
        whole_file = f.read()
    data = json.loads(whole_file)
    return data
    
def mergeAllJupyterFile(file=None, base=baseName):
    if not os.path.exists(base):
        create_baseFile(base)

    filehdr=file.replace(pathToYourLessonPlans,"")
    # read files
    Filename=base
    base_file = read_file_as_json(Filename)
    next_files = read_file_as_json(file)

    '''Create a header with each file to make a clear boundry among files'''
    FileBoundry =   {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Merged Jupyter Notebook"
   ]
   }
    
    FileBoundry['source'] = f'<hr><font color="green"><h1>from file: {filehdr[:-6]}</h1></font>'

    # merge cells of second file into base_file one with Name of file as a header
    base_file['cells'] = base_file['cells'] + [FileBoundry] + next_files['cells']

    # dump data in baseFile
    Filename = Filename
    with open(Filename,'w+') as f:
            f.write(json.dumps(base_file))
        
def create_base_for_results(base):
    '''This moves the merged file to log folder created for it'''
    # path to root log directory 
    root_logDir = os.path.join(os.curdir, "results_folder"+weekNo)

    run_id = time.strftime("mergedFile_%Y_%m_%d-%H_%M_%S")
    move_to_path = os.path.join(root_logDir, run_id)

    def move_file_sub_log_dir(base,move_to_path):
        '''This moves the baseFile to sub log directory'''
        # generate run id based on current time

        
        # path to move baseFile
        # move_to_path = os.path.join(root_logDir, run_id)
        if not os.path.isdir(move_to_path):
            os.makedirs(move_to_path)
        base_file = base
        
        # finally move baseFile
        import shutil
        shutil.move(base_file, move_to_path)
        print(f"\n## Access merged file at \
the following location ##\n{move_to_path}")
    
    move_file_sub_log_dir(baseName,move_to_path)
    GetResources.createResources(weekNo,dayNo,baseName,pathToYourLessonPlans,root_logDir)

class CleanExit(Exception):
    '''Protects program from stopping abruptly'''
    def __init__(self):
        print("\n## No jupyter notebooks found to merge ##")
        print("\nexiting program....")


def safelyExit():
    '''safely exit when target notebooks are not present'''
    import sys
    try:
        sys.exit()
    except:
        raise CleanExit

def is_target_notebooks_exists(listOfFiles):
    for file in listOfFiles:
        if ".ipynb" in file:
            return True
    return False

def main(listOfFiles):
	# get the list of all the files
    

    # remove unwanted files from list of files
    if '.ipynb_checkpoints' in listOfFiles:
        listOfFiles.remove('.ipynb_checkpoints')
    if "mergeJupyterFiles.ipynb" in listOfFiles:
        listOfFiles.remove('mergeJupyterFiles.ipynb')
            
    # check the existence of target notebook files
    if not is_target_notebooks_exists(listOfFiles):
    	safelyExit()
    	
	# iterate over the list of files to merge them
    listOfFiles.sort()
    for file in listOfFiles:
        if ".ipynb" in file:
            mergeAllJupyterFile(file,baseName)
    create_base_for_results(baseName)
        


main(createListOFiles(weekNo,dayNo))


