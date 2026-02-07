FROM python:3.12-slim
WORKDIR /app
COPY report.py .
ENTRYPOINT ["python3", "report.py"]
