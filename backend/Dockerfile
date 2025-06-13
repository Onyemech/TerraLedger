FROM python:3.10-slim WORKDIR /app

Install MySQL client libraries

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

Copy requirements and install dependencies

COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt

Copy the rest of the application

COPY . .

Run the application

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]