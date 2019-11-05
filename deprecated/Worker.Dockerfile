FROM gcr.io/ucb-datahub-2018/data100-user-image:6d8e675
RUN pip uninstall -y okpy
COPY worker.py worker-requirements.txt ./
RUN pip install -r worker-requirements.txt
