FROM python:3.9.6-alpine3.14
WORKDIR /app
ENV PYTHONPATH app/utils/
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000","app:app"]
