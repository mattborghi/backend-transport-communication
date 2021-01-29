# Publish/Subscribe

The assumption behind a work queue is that each task is delivered to exactly one worker. In the Publish/subscribe a message will be delivered to multiple consumers. 

![imag](https://www.rabbitmq.com/img/tutorials/python-three-overall.png)

## Temporary queues

We want to hear about all log messages, not just a subset of them. We're also interested only in currently flowing messages not in the old ones. To solve that we need two things.

Firstly, whenever we connect to Rabbit we need a fresh, empty queue. To do it we could create a queue with a random name, or, even better - let the server choose a random queue name for us. We can do this by supplying empty `queue` parameter to `queue_declare`:

```python
result = channel.queue_declare(queue='')
```

At this point `result.method.queue` contains a random queue name. For example it may look like `amq.gen-JzTY20BRgKO-HjmUJj0wLg`.

Secondly, once the consumer connection is closed, the queue should be deleted. There's an `exclusive` flag for that:

```python
result = channel.queue_declare(queue='', exclusive=True)
```

## Bindings

We've already created a fanout exchange and a queue. Now we need to tell the exchange to send messages to our queue. That relationship between exchange and a queue is called a *binding*.

```python
channel.queue_bind(exchange='logs',queue=result.method.queue)
```

From now on the `logs` exchange will append messages to our queue.