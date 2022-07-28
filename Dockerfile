FROM python:3.10-slim

WORKDIR /app

COPY ./static ./static
COPY ./templates ./templates
COPY config.ini main.py sudoku.py template.py require.txt ./

RUN pip install --no-cache-dir -r require.txt

CMD ["python", "main.py"]
