from logging_config import logger

from .m_connector import mysql_connector


@mysql_connector
def get_last_campaign_uuid(connector):
    logger.info("SELECTING LAST CAMPAIGN UUID")
    query = """
                SELECT DISTINCT
                    (mailwizz_campaign_uid) AS uuid
                FROM
                    tbl_customer_outreach_campaign_sent_listings
                ORDER BY
                    created_at DESC
                LIMIT
                    1
            """
    cursor = connector.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    logger.info(f"SQL RESPONSE - {data}")

    return data[0][0] if data else None



if __name__ == "__main__":
    get_last_campaign_uuid()