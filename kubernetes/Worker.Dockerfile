FROM gcr.io/ucb-datahub-2018/data100-user-image:119c524
RUN pip uninstall -y okpy
COPY worker.py worker-requirements.txt ./
RUN pip install -r worker-requirements.txt
