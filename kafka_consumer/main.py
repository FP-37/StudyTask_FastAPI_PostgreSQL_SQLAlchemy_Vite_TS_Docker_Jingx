import threading
import logging_consumer
import db_consumer

if __name__ == "__main__":
    t1 = threading.Thread(target=logging_consumer.main)
    t2 = threading.Thread(target=db_consumer.main)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
