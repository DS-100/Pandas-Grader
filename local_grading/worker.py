import os
import subprocess
import traceback
import zipfile
import sys
from io import StringIO

import click
import requests

import gofer.ok
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue

"""
Grade single assignment
"""

GRADING_DIR = os.getcwd()
ACCESS_TOKEN = ''
LOCAL_FILE_TO_GRADE = 'proj1a-alflsowl12.ipynb'


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

        print("MESSAGE")
        print(okpy_result["msg"])
        print("-----------SCORE--------------")
        print(okpy_result["total"])

    except Exception as e:
        print("Things went wrong")
        print("Exception: " + str(e))
        print("Stack trace")
        print(traceback.format_exc())
        print(e)

