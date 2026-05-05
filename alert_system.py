import logging
import datetime
import os
from fastapi import FastAPI
from pydantic import BaseModel

# Setup professional logging
LOG_FILE = "intrusion_alerts.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class AlertSystem:
    """
    Handles the silent notification and logging of honeyword hits.
    """
    def __init__(self):
        self.logger = logging.getLogger("HoneywordIDS")

    def trigger_alert(self, username: str, honeyword_used: str, ip_address: str):
        """
        Logs a critical security event when a honeyword is used.
        """
        alert_msg = (
            f"CRITICAL INTRUSION DETECTED | "
            f"User: {username} | "
            f"Honeyword Hit: {honeyword_used} | "
            f"Source IP: {ip_address} | "
            f"Timestamp: {datetime.datetime.now().isoformat()}"
        )
        self.logger.critical(alert_msg)

        # In a production system, this is where you would integrate:
        # - Sending an email to the admin
        # - Triggering a PagerDuty/Slack alert
        # - Flagging the account for manual review

# Singleton instance
alert_system = AlertSystem()
