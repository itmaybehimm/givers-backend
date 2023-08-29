FROM python:3.9

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=1

WORKDIR /api

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "sh","./entrypoint.sh" ]