# SHOULD EDIT to use the highest Python version with minimum image size that your program supports
FROM python:3.11-slim
WORKDIR /work

COPY pyproject.toml .
RUN pip install .

# MAY EDIT to install your dependencies other than Python

USER nobody
COPY . .

# MUST EDIT to execute your program
CMD python problem_awesome_problem/main.py
