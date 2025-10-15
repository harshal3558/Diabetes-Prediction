FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies (caches this layer unless requirements change)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your code
COPY . /app

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
