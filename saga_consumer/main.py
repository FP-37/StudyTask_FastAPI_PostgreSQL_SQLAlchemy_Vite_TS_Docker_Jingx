import threading
import saga_consumer
import saga_logger

if __name__ == "__main__":
    t1 = threading.Thread(target=saga_consumer.main)
    t2 = threading.Thread(target=saga_logger.main)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
