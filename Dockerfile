FROM python:3.11

WORKDIR /speechpal-mvp

COPY requirements.txt requirements.txt
COPY bot.py bot.py
COPY server.py server.py
COPY run.sh run.sh
COPY processing processing
COPY util util

# Args
ARG BOT_TOKEN
ARG OPENAI_API_KEY
ARG OPENAI_ORG

# Env vars
ENV BOT_TOKEN=$BOT_TOKEN
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV OPENAI_ORG=$OPENAI_ORG

EXPOSE 8080

RUN apt-get update && apt-get install ffmpeg -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U git+https://github.com/PrithivirajDamodaran/Gramformer.git
RUN python -m spacy download en

CMD ["./run.sh"]
