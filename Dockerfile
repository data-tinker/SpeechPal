FROM python:3.11

WORKDIR /speechpal-mvp

# Args
ARG BOT_TOKEN
ARG OPENAI_API_KEY
ARG OPENAI_ORG

# Env vars
ENV BOT_TOKEN=$BOT_TOKEN
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV OPENAI_ORG=$OPENAI_ORG
ENV MONGO_DB_CONNECTION=$MONGO_DB_CONNECTION

EXPOSE 8080

RUN apt-get update

# Install ffmpeg
RUN apt-get install ffmpeg -y

# Install phantomjs
COPY scripts scripts
RUN apt-get install build-essential chrpath libssl-dev libxft-dev -y
RUN apt-get install libfreetype6 libfreetype6-dev  -y
RUN apt-get install libfontconfig1 libfontconfig1-dev -y
RUN scripts/install-phantomjs 2.1.1

# Install python modules
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U git+https://github.com/PrithivirajDamodaran/Gramformer.git

COPY bot.py bot.py
COPY server.py server.py
COPY run.sh run.sh
COPY processing processing
COPY persistence persistence
COPY steps steps
COPY util util

CMD ["./run.sh"]
