# ThingSpeaks Data Engine

An data engine to fetch and normalize data from [ThingSpeaks platform](https://thingspeak.com/) 

- [Local Setup](#local-setup)
- [Use the software](#Use-the-software)

## Local Setup
I am using [docker-compose](https://docs.docker.com/compose/) like a container orchestration for the data engine, mysql database and adminer(GUI for mysql) Please follow these steps:

First, Install docker and [docker-compose](https://docs.docker.com/compose/install/)  on your OS.

Then modify the .env like your needs:
```bash
cd app
cp .env_example .env
```

For this example, i am using [this](https://thingspeak.com/channels/1350261) public channel about quality air on germany location.

Now, you need to setup your database sql script with the table and fields where is going to store the data.

```bash
vim database.sql
```

All done, let´s use the software!!!

## Use the software

Now with your environment ready, we can run the app:

```bash
docker-compose up
```
This will build the engine and execute all the containers for us, to check if all is fine, just execute:

```bash
docker ps
```
Now you need to check that all the containers have the status Up. The engine will be execute and insert your data to the mysql database, you can acess it through the adminer, just type `http://localhost:8081/` on your browse. The database name is `data_sensors` and the credencials are mysql default `root`

All done!!
If you have any doubt or suggestion, please contact me `benjamin.zavaleta@grieletlabs.com`