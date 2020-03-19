# Website statuses aggregator
Service that checks websites availabilities

#Development
## Run project locally

Project was build using python 3.7
To install all dependencies, use:

```
pip install -r pip-dep/requirements.txt
```

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

Kafka image and utility functions uses code from 
[Wurstmeister](https://github.com/wurstmeister/kafka-docker) kafka-docker project
