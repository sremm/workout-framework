""" simple consumer endpoint with pika client for rabbit mq"""

import pika, sys, os


def main():
    pass
    ## connect to channel
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    # channel = connection.channel()

    # channel.queue_declare(queue="hello")

    ## define callback - these will map to import
    # def callback(ch, method, properties, body):
    #     print(" [x] Received %r" % body)

    # channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    # print(" [*] Waiting for messages. To exit press CTRL+C")
    # channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)