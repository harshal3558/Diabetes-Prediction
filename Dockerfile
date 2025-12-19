# FROM python:3.10-slim

# WORKDIR /app

# # Copy only requirements first for caching
# COPY requirements.txt /app/requirements.txt

# # Upgrade pip and install dependencies (caches this layer unless requirements change)
# RUN pip install --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # Now copy the rest of your code
# COPY . /app

# EXPOSE 8080

# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]



# =========================
# 1. Base image
# =========================
FROM python:3.10-slim

# =========================
# 2. Environment settings
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# 3. Set working directory
# =========================
WORKDIR /app

# =========================
# 4. Install system dependencies
# (required for numpy, pandas, sklearn)
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# =========================
# 5. Copy requirements first (Docker cache optimization)
# =========================
COPY requirements.txt .

# =========================
# 6. Install Python dependencies
# =========================
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# 7. Copy project files
# =========================
COPY . .

# =========================
# 8. Expose port (Flask/FastAPI)
# =========================
EXPOSE 5000

# =========================
# 9. Run application
# =========================
# CMD ["python", "application.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:app"]
