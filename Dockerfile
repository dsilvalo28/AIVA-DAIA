FROM python:3.7
COPY . /
RUN pip install -r requirements.txt
CMD python src/Application.py