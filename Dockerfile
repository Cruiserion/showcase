FROM python:3.8

RUN apt update && apt -y upgrade

# Install python packages
COPY ./app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
