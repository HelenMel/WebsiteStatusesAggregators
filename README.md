# Website statuses aggregator
Service that checks websites availabilities

#Development
## Run project locally

Project require Postgres and Kafka running on development machine.
To start it run:

```
  docker-compose up
 ```

This will start local Postgres and Kafka containers.

To check data in Postgres use:

```
docker-compose run db bash

psql --host=db --username=developer --dbname=website_statuses
```

