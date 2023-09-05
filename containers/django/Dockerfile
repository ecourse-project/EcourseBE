# Pull base image
FROM python:3.10

# Set environment variables
#ENV PIP_DISABLE_PIP_VERSION_CHECK 1
#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /api

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]