# Running RabbitMQ Server using Docker

```sh
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Install Python dependencies

```sh
cd rabbit-mq
pipenv shell
pipenv install
```

and run it with

```sh
python folder/file.py
```

## Install Julia dependencies

```sh
cd rabbit-mq
julia
Press ']' key
activate .
(rabbit-mq) instantiate
```

and run it with 

```sh
julia --project='.' folder/file.jl
```
