# powerdns-admin-docker

Published to https://hub.docker.com/r/hmcts/powerdns-admin

Building:
```bash
$ docker build -t hmcts/powerdns-admin .
```

Example usage:
```yaml
---

version: '2.1'

services:
  postgres:
    image: postgres:9.6-alpine
    command: postgres -c 'max_connections=250'
    volumes:
      - ./docker/database/init-db-v9.6.sh:/docker-entrypoint-initdb.d/init-db.sh
      - shared-database-data:/var/lib/postgresql/data
    healthcheck:
      test: psql -c 'select 1' -d postgres -U postgres
      retries: 40
    mem_limit: 320m
    memswap_limit: 0
    ports:
      - 5420:5432
  pdns:
    image: psitrax/powerdns
    environment: 
      AUTOCONF: postgres
      PGSQL_USER: pdns
      PGSQL_PASS: pdns
      PGSQL_HOST: postgres
      PDNS_DEFAULT_SOA_NAME: root.platform.hmcts.net
      PDNS_API: 'yes'
      PDNS_API_KEY: changeme
      PDNS_WEBSERVER: 'yes'
      PDNS_WEBSERVER_ADDRESS: '0.0.0.0'
      PDNS_WEBSERVER_ALLOW_FROM: '0.0.0.0/0'
    ports:
      - 8081:8081
  pdns-ui:
    image: hmcts/powerdns-admin
    environment: 
      PDA_DB_USER: 'pdns_ui'
      PDA_DB_PASSWORD: 'pdns_ui'
      PDA_DB_NAME: 'pdns_ui'
      PDA_DB_HOST: 'postgres'
      PDA_DB_PORT: 5432
      SAML_ENABLED: 'true'
      SAML_METADATA_URL: 'https://login.microsoftonline.com/rpe899.onmicrosoft.com/FederationMetadata/2007-06/FederationMetadata.xml'
      SAML_GROUP_ADMIN_NAME: '356b57d8-84f4-457a-b49e-9500820c0b2d'
      SAML_GROUP_TO_ACCOUNT_MAPPING: '9189d86a-e260-4c3d-8227-803123cdce84=cnp'
      SAML_SP_ENTITY_ID: 'https://rpe899.onmicrosoft.com/384ce2b5-fbd1-43db-9621-80394401edfb'
      PDNS_API_KEY: changeme
      PDNS_HOST: 'pdns'
      PDNS_PORT: '8081'
      PDA_SITE_NAME: 'HMCTS'
    ports: 
      - 5000:5000

volumes:
  shared-database-data:  
```

To release this you need to manually push to docker hub, automated build creation is broken.
I've contacted docker support, and there's a GitHub issue which is getting no response
