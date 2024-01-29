# Get to know with Apache Kafka
Kafka is an open-source message broker or distributed event streaming platform. It acts like a high-speed messaging system for data, allowing us to publish and subscribe to streams of real-time information. Kafka popular for building real-time data pipelines, streaming analytics applications, and mission-critical systems that need to handle large volumes of data at high speeds. 

### Why Kafka?
- **Scalable**: Can handle increased loads effectively.
- **High Performance**: Swiftly processes large volumes of data.
- **Persistent**: Data is stored on disk, ensuring safety in case of delivery failures.

### How to install Kafka
1. Install latest Java from [Eclipse Temurin](https://adoptium.net/temurin/releases/?os=any) because it is free and easy to install
2. Download latest kafka from their official [website](https://kafka.apache.org/downloads)
3. Extract Kafka file
4. By default, Kafka data is saved to /tmp/kraft-combined-logs. However, on Linux or Mac, this folder gets removed upon restarting. Therefore, it is recommended to modify the log.dirs setting in the server.properties file. Create a new folder in kafka directory, ex `data`, go to config > craft > server.properties and change log.dirs to data
   ```
   log.dirs=data
   ```
6. After creating data directory, we need to format a new directory using kafka-storage file by running the following code in the terminal.
   ```
   #get random uuid
   ./bin/windows/kafka-storage.bat random-uuid

   #format directory
   ./bin/windows/kafka-storage.bat format --cluster-id <generated random-uuid> --config config/kraft/server.properties
   ```
   > Disclaimer: This repository is designed for Windows. For MacOS and Linux, execute the bash file located in the ./bin directory with the same name.

7. Start Kafka by using kafka-server-start by running the following code
```
./bin/windows/kafka-server-start.bat config/kraft/server.properties
```

### Topic
When sending data to Kafka, it's essential to direct it to a specific Topic. A Topic is akin to a table in a database, serving as a storage space for data sent by producers. To create a Topic, the Kafka-topic file can be employed.
```
./bin/windows/kafka-topics.bat --bootstrap-server <connection>:<port> --create --topic <string>
```
for example
```
./bin/windows/kafka-topics.bat --bootstrap-server localhost:9092 --create --topic explore-kafka
```
You can list your kafka topic by using the following code
```
./bin/windows/kafka-topics.bat --bootstrap-server localhost:9092 --list
```
If you want to delete some topic, you can write the following code
```
./bin/windows/kafka-topics.bat --bootstrap-server localhost:9092 --delete --topic <topic name>
```
> Note: In my case (Windows), there is a bug causing the broker to crash after deleting a specific topic. I had to delete the data folder and perform formatting from scratch.

### Message

Data sent to a Kafka topic is called a `Message`, consisting of:

- `Topic` to store the topic name
- `Partition` to store the partition number where the Message will be stored
- `Header` containing additional information for the Message
- `Key` serving as the message ID. Unlike a Primary key in a database, Kafka keys can be the same across Messages
- `Value` representing the data content of the Message

### Log
Data in a Kafka Topic is stored in a `Log` format. The log is a simple method of storage, employing an `append-only` approach, meaning data only grows in accordance with the sequence of incoming data. This characteristic contributes to the swift data storage process in Kafka, as it involves appending data to the end only.

### Producer
A `Producer` is responsible for sending Messages to Kafka. Each Message sent is stored at the last sequence. Kafka provides a simple Console `Producer` application in the `kafka-console-producer.bat` file.
```
kafka-console-producer.bat --bootstrap-server <host:port> --topic <topic name>
```
in my case
```
./bin/windows/kafka-console-producer.bat --bootstrap-server localhost:9092 --topic explore-kafka
```
After that, you can send your own messages



### Consumer
A Consumer is an application that receives data from a Kafka producer. The reading process is sequential from the earliest to the latest Message. To run the Console Consumer, use the `kafka-console-consumer` file.
```
kafka-console-consumer.bat --bootstrap-server <host:port> --topic <string> --from-begininng
```
in my case,
```
./bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic explore-kafka --from-beginning
```

### Consumer Group
When a Consumer reads data from a Topic, a `Consumer Group` is automatically created. However, in a real application, we need to explicitly choose the `Consumer Group` to use. Typically, the `Consumer Group` uses its application name.

#### Without mentioning Consumer Group
Automatically creates a new `Consumer Group`. Automatically generated `Consumer Group`s by Kafka will always be unique. If `Consumer Group`s are always different, data will be received repeatedly
  
#### Using Consumer Group
Consumers in the same `Consumer Group `become a unit Data from the topic won't be sent repeatedly, only once to one consumer in the same group


To use a Consumer group, add the `--group <group name>` property:
```
./bin/windows/kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic explore-kafka --group kafka-group
```

#### When no active consumer and data keeps coming, where will the consumer read data when started?
By default, the consumer reads only new data. However, use '--from-beginning' to read data from the beginning. If the consumer has read data up to, say, number 5, then is turned off and restarted when data sent is at number 11, the consumer will read from number 6 onwards due to the 'offset'.

### Offsett
Kafka stores information about the last read data, known as `Offset`. When a consumer is first run, it doesn't have an `offset` and needs to specify `--from-beginning` or read from new data. The `offset` information is stored in the Consumer Group. Therefore, when running a consumer with a different Consumer Group, previous `offset` data is not available.

### Partition
When creating a Kafka topic, the data is stored in partitions. By default, the number of partitions is 1. Each partition can only be read by one consumer. To allow multiple consumers to receive data simultaneously, Kafka can store data in several partitions.

To create a topic with a specific number of partitions:
```
kafka-topics.bat --bootstrap-server <host:port> --create --topic <topic-name> --partition <number>
```
To add partitions to an existing topic:
```
kafka-topics.bat --bootstrap-server <host:port> --alter --topic <topic-name> --partitions <number>
```
To view information about a created topic:
```
kafka-topics.bat --bootstrap-server <host:port> --describe --topic <topic-name>
```
However, even with increased partitions, the number of consumers receiving data in the same consumer group remains 1. This is because we haven't implemented `routing`.

### Routing
The determination of which partition will receive data is based on the `Key` of the sent Message. Previously, we sent data using the Console Producer without setting a `Key`, so the default `Key` is Null. Consequently, data will always be sent to the same partition.

#### Key Routing
When determining which partition to select, Kafka uses the formula:

$$hash(message.key)\% totalpartition $$

Misalnya, 
$$ hash(example) = 9$$
$$ 9 \%2=1$$
Data will be stored in Partition 1. Therefore, data with the same key will be stored in the same partition.

#### Console Producer
By default, the Console Producer uses a null Key when sending data. If you want to use a Key, add the parameters `--property "parse.key=true"` `--property"key.separator=:"`
With this properties, you can send `Key` and `Message` separated by `:`

```
kafka-console-producer.bat --bootstrap-server <host:port> --topic <topic-name> --property "parse.key=true" --property "key.separator=:"
```
in my case,
```
kafka-console-producer.bat --bootstrap-server localhost:9092 --topic explore-kafka --property "parse.key=true" --property "key.separator=:
```
Example of sending data:
```
firstkey:This is the first message
firstkey:and this is the second image
secondkey:This one is the first message for second key
```

#### Console Consumer
To view the Key in Messages when creating a console consumer, add the command `--property "print.key=true"`.

```
kafka-console-consumer.bat --bootstrap-server <host:port> --topic <topic-name> --group <group-name> --from-beginning --property "print.key=true"
```
in my case,
```
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic explore-topic --group kafka-group --from-beginning --property "print.key=true"
```

***

# Reference
https://www.youtube.com/watch?v=K7bIgpPAdbc&t=3371s

# Kafka Implementation using Python

The reference below is still being explored because the consumer file is not displaying the messages as expected in my current implementation.

- https://www.youtube.com/watch?v=Q4XA5nUpLeo
- https://kafkaide.com/learn/how-to-start-using-apache-kafka-in-python/