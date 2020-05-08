1. This assumes you have pandas, jupyter, etc set up locally. If not, you can also do this on datahub by uploading `worker.py` to an empty folder first. 

2. Install the data100 gofer-grader by running `pip install --user git+https://github.com/DS-100/Gofer-Grader.git@plain_text_repr`. Depending on how you have python set up you may need to use pip3 instead of pip. 

3. Copy over all the files and folders inside `dist/.../<assignment>/autograder` to this folder. 

4. Put the student's `.ipynb` file into this folder 

5. In `worker.py`, modify `LOCAL_FILE_TO_GRADE` to the filename of the student's file, and then run `worker.py` 

6. Copy over the outputted message and score to the students `regrade` field in Okpy. 

7. Clear out this folder between grading different assignments, e.g switching from regrading HW3 to Proj1 submissions. For this reason, it's best to handle all regrades for each assignment in bulk.

8. If you see an error involving `lxml`, run `pip uninstall lxml` and then `pip install lxml`. You may have to use `pip3`. 