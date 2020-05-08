import os
import subprocess
import traceback
import zipfile
import sys
import shutil

import click
import requests

import gofer.ok
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue

"""
Grade single assignment
"""

DEV_PATH = '/Users/wwhuang/Dropbox/git/sp20-dev/dist/'
ASSIGNMENT_TYPE = 'hw'
ASSIGNMENT_NUM = '4'
LOCAL_FILE_TO_GRADE = 'hw4.ipynb'

GRADING_DIR = os.getcwd()
ACCESS_TOKEN = ''


assignment_path = DEV_PATH + ASSIGNMENT_TYPE + '/' + ASSIGNMENT_TYPE + ASSIGNMENT_NUM + '/autograder/'


def get_gofer_grade(fname, q):
    r = gofer.ok.grade_notebook(fname)
    q.put(r)

def gofer_wrangle(res):
    # unique-ify the score based on path
    path_to_score = {}
    total_score = 0
    for r in res:
        key = r.paths[0].replace(".py", "")
        if key not in path_to_score:
            total_score += r.grade
        path_to_score[key] = r.grade
    okpy_result = {"total": total_score, "msg": "\n".join(repr(r) for r in res)}
    return okpy_result, path_to_score

if __name__ == '__main__':    

    try:
        os.chdir(GRADING_DIR)
        shutil.copyfile(LOCAL_FILE_TO_GRADE, assignment_path + LOCAL_FILE_TO_GRADE)
        os.chdir(assignment_path)
        print("STARTING THINGS UP ")
        result = gofer.ok.grade_notebook(LOCAL_FILE_TO_GRADE)
        print("DONE USING NEW CONTEXT", flush=True)
        print(result)
        okpy_result, path_to_score = gofer_wrangle(result)

        score_content = {
            "score": okpy_result["total"],
            "kind": "Autograder",
            "message": okpy_result["msg"],
        }

        print("-----------MESSAGE--------------")
        print(okpy_result["msg"])
        print("-----------SCORE--------------")
        print(okpy_result["total"])

    except Exception as e:
        print("Things went wrong")
        print("Exception: " + str(e))
        print("Stack trace")
        print(traceback.format_exc())
        print(e)

