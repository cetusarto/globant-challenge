FROM python:3.10

ENV DATABASE_URL=postgresql://API:Globant@10.16.176.3:5432/hiring

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
