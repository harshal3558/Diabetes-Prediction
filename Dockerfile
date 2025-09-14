# FROM  python:3.12-alpine
# WORKDIR /code
# ENV FLASK_APP=application.py
# ENV FLASK_RUN_HOST=0.0.0.0
# COPY . .
# RUN pip install -r requirements.txt
# EXPOSE 5000
# CMD ["flask","run"]


FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=application.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]