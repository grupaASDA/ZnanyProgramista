FROM python:3.11-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /ZnanyProgramista
COPY . .
RUN pip install -r requirements.txt

# Load environmental variables from .env file
ARG ENV_FILE

# Run migration commands and start the server
RUN python manage.py makemigrations accounts communication programmers
RUN python manage.py migrate
RUN python manage.py loaddata initial_db.json
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
