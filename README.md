# Data 100 Autograder
This is Data100's okpy compatible autograder. A Django server interaces with Okpy's servers, and spawns kubernetes jobs on the data100-staging namespace that grade each submission.

## Proccess 
1. Set up the dockerhub image in the `kubernetes` folder.
2. Set up a postgres db for the autograder to use, according to the settings in `pandas_grader/settings.py`. 
	- See <https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04> for instructions.
3. Run the django server using `python pandas_grader/manage.py runserver 0.0.0.0:8080`. 
	- We use django-admin for our web interface. 
3. The server uses [Constance](https://github.com/jazzband/django-constance) to manage settings. Default values can be found in `pandas_grader/settings.py` Values can be changed `Config` link in the main web interface.
4. Create an assignment in the `Assignments` link in the web interface. You upload the `autograder` output of jassign here, and get the autograder key for okpy from here. 
5. Put the autograder key into Okpy (make sure you have the autograder endpoint set up), and run the grading job. 
6. In the `grading jobs` assignments, figure out how many assignments are still in the `queued` state, and spin up a bunch of workers to handle these. See `pandas_grader/urls.py`
7. After a while, most of the grades will finish, but some will fail. You can see what students with submissions did not get a grade under the "View Scores" tab in the okpy assignment page. 
8. Re-run any student submissions that did not get graded the first time around. 
9. Clean up the pods and jobs!

## Troubleshooting 

Submissions tyically fail for one of three reasons: the autograder hands out the same assignment to multiple pods, a pod fails to get the assignment from okpy (no automatic retries), or the assisgnment itself fails. 

Right now you solve the first two problems by creating more pods, and manually submitting autograder requests for students from okpy. 

The most common reason for the assignment itself failing was that students would use a variable named `check`, which conflicted with a function call in our verison of gofer-grader. I've since switched our function to be called `gofer_check`, so hopefully this resolves the problem. Otherwise, you will have to figure out where the code is stalling manually. 

