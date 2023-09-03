FROM python:3.9-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY culture_bot/ /app

WORKDIR /app

CMD ["gunicorn", "culture_bot.wsgi:application", "--bind", "0:8000"]