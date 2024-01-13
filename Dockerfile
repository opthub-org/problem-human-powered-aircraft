FROM python:3.11-slim
WORKDIR /work
COPY . /work
RUN pip install -r requirements.txt
CMD python problem_human_powered_aircraft/main.py
