FROM python:3.9-slim as python-deps

RUN pip install pipenv
COPY Pipfile /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

FROM python-deps AS production 

ENV FXDATA_URL  127.0.0.1
# install app into container
WORKDIR /app
COPY /app .
COPY entrypoint.sh /usr/bin/

# Run the app
ENTRYPOINT ["entrypoint.sh"]


FROM python-deps AS dev 

ENV FXDATA_URL  127.0.0.1
# install app into container
WORKDIR /app
COPY /app .
COPY entrypoint.sh /usr/bin/

# Run the app
ENTRYPOINT ["entrypoint.sh"]