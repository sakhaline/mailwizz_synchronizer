from .p_connector import postgres_connector

from logging_config import logger


@postgres_connector
def insert_mailwizz_campaign_data(connector, insert_data: tuple):
    logger.info("INSERTING MAILWIZZ DATA TO statistics.mailwizz_campaigns")
    query = """
        INSERT INTO statistics.mailwizz_campaigns
            (
            campaign_uid,
            name,
            status,
            type,
            bounces_count,
            campaign_status,
            clicks_count,
            complaints_rate,
            delivery_error_count,
            delivery_error_rate,
            delivery_success_count,
            delivery_success_rate,
            hard_bounces_count,
            hard_bounces_rate,
            internal_bounces_count,
            internal_bounces_rate,
            opens_count,
            opens_rate,
            processed_count,
            soft_bounces_count,
            soft_bounces_rate,
            subscribers_count,
            unique_clicks_count,
            unique_clicks_rate,
            unique_opens_count,
            unique_opens_rate,
            unsubscribes_count,
            unsubscribes_rate,
            clicks_rate,
            complaints_count
            )
            VALUES
            (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s
            );
        """
    cursor = connector.cursor()
    cursor.execute(query, insert_data)
    connector.commit()
    return True