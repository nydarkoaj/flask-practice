FROM python:3.13-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY website ./website

# Enquiries are written here; mount a volume to keep them between deploys
ENV ENQUIRY_DIR=/data
VOLUME ["/data"]

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
