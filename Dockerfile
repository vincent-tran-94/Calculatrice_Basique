FROM python:3.10.0-alpine
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python3","main.py"]
