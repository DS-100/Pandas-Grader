import os
import subprocess
import traceback
import zipfile
from contextlib import redirect_stderr, redirect_stdout
import sys
from io import StringIO

import click
import requests
from ansi2html import Ansi2HTMLConverter

import gofer.ok
import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue

GRADING_DIR = os.getcwd()


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


@click.command()
@click.option("--api-url", required=True)
def main(api_url):
    cont = True
    while(cont):
        log_buffer = StringIO()
        conv = Ansi2HTMLConverter()
        try:
            print("Worker starting")
            print("api_url: " + str(api_url))
            r = requests.get(f"{api_url}/api/ag/v1/fetch_job")
            print("Request response: " + r.text)
            fetched = r.json()
            print("fetched " + str(fetched))
            if fetched["queue_empty"]:
                print("Queue empty 1")
                cont = False
                break
            
            skeleton_name = fetched["skeleton"]
            skeleton_zip = requests.get(f"{api_url}/api/ag/v1/skeleton/{skeleton_name}")

            os.makedirs(GRADING_DIR, exist_ok=True)
            with open(f"{GRADING_DIR}/{skeleton_name}.zip", "wb") as f:
                f.write(skeleton_zip.content)

            proc = subprocess.Popen(["unzip", "-o", skeleton_name], cwd=GRADING_DIR)
            proc.wait()
            assert proc.returncode == 0, "Unzip failed"

            access_token = fetched["access_token"]
            backup_id = fetched["backup_id"]
            job_id = fetched["job_id"]
            backup_assignment_url = f"https://okpy.org/api/v3/backups/{backup_id}?access_token={access_token}"
            backup_response = requests.get(backup_assignment_url)
            backup_json = backup_response.json()
            try:
                file_dict = backup_json["data"]["messages"][0]["contents"]
            except Exception as e:
                print("Something went wrong with getting the file dict")
                print("Backup Assignment URL")
                print(backup_assignment_url)
                print("Backup response:")
                print(backup_response.text)
                print("Backup json:")
                print(backup_json)
                print(e, flush=True)
                cont = False
                break

            files_to_grade = []
            for name, content in file_dict.items():
                if name == "submit":
                    continue
                files_to_grade.append(name)
                with open(f"{GRADING_DIR}/{name}", "w") as f:
                    f.write(content)
            assert len(files_to_grade) == 1, "Only support grading 1 notebook file"

            os.chdir(GRADING_DIR)

            # Do the grading in another context to avoid name space collisions and the like 
            # Should really add change the autograder to do this.
            print("MAKE NEW CONTEXT", flush=True)
            ctx = mp.get_context('spawn')
            q = ctx.Queue()
            p = ctx.Process(target=get_gofer_grade, args=(files_to_grade[0],q,))
            p.start()
            p.join() # this blocks until the process terminates
            result = q.get()
            print("DONE USING NEW CONTEXT", flush=True)
            print(result)
            log_buffer.write(str(result))
            okpy_result, path_to_score = gofer_wrangle(result)
            # print(res)
            path_to_score["bid"] = backup_id
            path_to_score["assignment"] = skeleton_name
            #report_breakdown_url = f"{api_url}/api/ag/v1/report_result"
            #requests.post(report_breakdown_url, json=path_to_score)

            score_content = {
                "bid": backup_id,
                "score": okpy_result["total"],
                "kind": "Autograder",
                "message": okpy_result["msg"],
            }
            score_endpoint = (
                f"https://okpy.org/api/v3/score/?access_token={access_token}"
            )
            resp = requests.post(score_endpoint, json=score_content)
            assert resp.status_code == 200, resp.json()
        except Exception as e:
            print("Things went wrong")
            print("Exception: " + str(e))
            print("Stack trace")
            print(traceback.format_exc())
            print(e)
            cont = False
            break

        #print(log_buffer.getvalue())
        print("Pandas Version: " + str(pd.__version__), file=sys.stderr)
        print("Sending log to api/ag/v1/report_done")

        report_done_endpoint = f"{api_url}/api/ag/v1/report_done/{job_id}"
        resp = requests.post(report_done_endpoint, data=conv.convert(log_buffer.getvalue()))
        
        if resp.status_code == 200: 
            print("Everything Successful")
        else: 
            print("Response error code: " + str(resp.status_code))
            cont = False
            break


if __name__ == "__main__":
    try:
        main()
        #cont = True
        #while(cont):
        #    cont = main()
        #    print(cont)

    except Exception as e:
        traceback.print_exc()
