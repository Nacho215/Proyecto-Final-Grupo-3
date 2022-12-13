FROM python:slim

RUN apt-get update \
&& apt-get install -y --no-install-recommends git \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

RUN git clone --branch main --depth 1 https://github.com/Nacho215/Proyecto-Final-Grupo-3.git /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python" ,"setup.py" ]

