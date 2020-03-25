# Website statuses aggregator


Service that checks websites availabilities

Currently it checks two predefined websites: `www.verkkokauppa.com` and www.verkkokauppa.com`

Project has two parts: producer and consumer.
Producer check websites statuses and stores it to kafka
to start producer, run:


```
pip install ./producer
python -m producer
```

Consumer listen to website statuses kafka topic and stores them to postgres
```
pip install ./consumer
python -m consumer
```

### !!! Both require access to remote services. !!! ###

Both services could be configured using configuration file

Prod environment connect to remote kafka and postgresql services 
 and requires kafka certificates and key stored in `HOME/kafka/cert/` folder and
 postgresql service password stored `HOME/kafka/pass/avnadm.pgpass`


#Setup development environment

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
