FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data
EXPOSE 8501
ENV LAB_DB=/app/data/lab.db
CMD ["streamlit","run","app.py","--server.address=0.0.0.0"]
