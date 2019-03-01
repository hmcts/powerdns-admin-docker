FROM alpine:3.9 as builder

RUN set -xe; \
    apk add --no-cache nodejs python3 supervisor yarn xmlsec netcat-openbsd postgresql-client; \
    pip3 install --upgrade pip

RUN wget -O powerdns-admin.tar.gz https://github.com/timja/PowerDNS-Admin/archive/6b1282e710a4031659ed340ca7ef0518b4893f89.tar.gz \
    && tar -xzf powerdns-admin.tar.gz \
    && mv PowerDNS-Admin-* /powerdns-admin/ \
    && rm powerdns-admin.tar.gz

WORKDIR /powerdns-admin

RUN set -xe; \
    apk add --no-cache --virtual _build alpine-sdk libffi-dev xmlsec-dev python3-dev openldap-dev mariadb-connector-c-dev postgresql-dev; \
    pip3 install -r requirements.txt; \
    pip3 install psycopg2==2.7.7; \
    apk del _build 

RUN set -xe; \
    adduser -Su 50 -s /sbin/nologin www-data; \
    addgroup -Sg 50 www-data; \
    adduser www-data www-data; \
    mkdir /powerdns-admin/logs ; \
    chown -R www-data:www-data /powerdns-admin/ ; \
    yarn install --pure-lockfile

USER www-data

# config is required but using the default for assets build to reduce time spent
# waiting for flask assets to build on custom config changes
RUN cp /powerdns-admin/config_template.py /powerdns-admin/config.py
RUN flask assets build

COPY ./config.py /powerdns-admin/config.py
COPY ./entrypoint.sh /entrypoint.sh

EXPOSE 9191 9393

ENTRYPOINT ["/entrypoint.sh"]
