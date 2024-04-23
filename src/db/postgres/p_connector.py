import os

import psycopg2
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder

from logger.logging_config import logger as logging

load_dotenv()

SSH_MODE = int(os.getenv("SSH_MODE"))
SSH_PKEY = os.getenv("SSH_PKEY")

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

SSH_USERNAME = os.getenv("SSH_POSTGRES_USERNAME")
SSH_SERVER_ADDRESS=os.getenv("SSH_POSTGRES_SERVER_ADDRESS")
SSH_SERVER_PORT = int(os.getenv("SSH_POSTGRES_SERVER_PORT"))
LOCAL_PORT = os.getenv("POSTGRES_LOCAL_PORT")


def postgres_connector(func):
    """
    decorator that connects to Postgres DB and executes inputted query handler; handles exceptions
    """
    def inner(*args, **kwargs):
        logging.debug(f"CONNECTING TO POSTGRES WITH SSH MODE {SSH_MODE}")

        if SSH_MODE == 1:
            # starting SSH tunnel
            server = SSHTunnelForwarder(
                (SSH_SERVER_ADDRESS, SSH_SERVER_PORT),
                ssh_username=SSH_USERNAME,
                ssh_pkey=SSH_PKEY,
                remote_bind_address=(POSTGRES_HOST, int(POSTGRES_PORT)),
                local_bind_address=("localhost", int(LOCAL_PORT))
            )
            server.start()
            logging.debug("POSTGRES SSH TUNNEL STARTED")

            conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER,
                                    password=POSTGRES_PASSWORD, host="localhost", port=LOCAL_PORT)
        else:
             conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER,
                                    password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
        
        logging.debug(f"CONNECTED TO POSTGRES")
        try:
            return func(conn, *args, **kwargs)
        except Exception as ex:
            logging.error(f"!!! POSTGRES ERROR -- {ex}")
        finally:
            conn.close()
            logging.debug("POSTGRES DISCONNECTED")
            if SSH_MODE == 1:
                server.stop()
                logging.debug("POSTGRES SSH TUNNEL DISCONNECTED")

    return inner


# demo postgres_connector decorator use case
@postgres_connector
def postgres_demo_query(connector):
    curr = connector.cursor()
    curr.execute("SELECT * FROM statistics.market_leader_polygons LIMIT 1")
    data = curr.fetchall()
    curr.close()
    logging.info(data)
    return data


if __name__ == "__main__":
    postgres_demo_query()