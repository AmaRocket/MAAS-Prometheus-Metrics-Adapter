FROM python:3.10-slim

WORKDIR /adapter

COPY metrics_adapter.py .

RUN pip install flask requests

EXPOSE 8001

CMD ["python", "metrics_adapter.py"]