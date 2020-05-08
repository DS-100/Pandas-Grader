Whether or not this is run locally or on datahub, install the data100 gofer-grader by running `pip install --user git+https://github.com/DS-100/Gofer-Grader.git@plain_text_repr`. Depending on how you have python set up you may need to use pip3 instead of pip. 

If you see an error involving `lxml`, run `pip uninstall lxml` and then `pip install lxml`. You may have to use `pip3`. 

For `auto_worker.py`: 

1. This assumes you have sp20-dev checked out wherever you are running these files.   

2. Set `DEV_PATH`, `ASSIGNMENT_TYPE`, `ASSIGNMENT_NUM`, and `LOCAL_FILE_TO_GRADE` to the appropriate values. 
`DEV_PATH` is the filepath to the `dist` folder in `sp20-dev`. 
`ASSIGNMENT_TYPE` is lab, hw, or proj. 
`ASSIGNMENT_NUM` is the assignment number, such as `1`, `2a`. No capitals, and must match the folder names in `dist`, so you might need to write `02` instead of `2`.
`LOCAL_FILE_TO_GRADE` is the filepath to the students submission you are grading.

3. Run `auto_worker.py`. If the paths are set correctly, the script will copy the students assignment over to 
the appropriate `autograder` folder in `dist`, and then grade the assignment.

4. Copy the message and score to the students `regrade` and `total` fields in Okpy. 

For `worker.py`:

1. This can be easily set up either localy or by copying worker.py to datahub, but requires more manual copying of files.

3. Copy over all the files and folders inside `dist/.../<assignment>/autograder` to this folder. 

4. Put the student's `.ipynb` file into this folder 

5. In `worker.py`, modify `LOCAL_FILE_TO_GRADE` to the filename of the student's file, and then run `worker.py` 

6. Copy over the outputted message and score to the students `regrade` and `total` fields in Okpy. 

7. Clear out this folder between grading different assignments, e.g switching from regrading HW3 to Proj1 submissions. For this reason, it's best to handle all regrades for each assignment in bulk.

