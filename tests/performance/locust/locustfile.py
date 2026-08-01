import random

from locust import HttpUser, between, task


class PlatformUserSimulator(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def check_command_handler(self):
        self.client.get("http://localhost:8000/health", name="/command-handler/health")

    @task(5)
    def simulate_smartlead_webhook(self):
        payload = {
            "account_id": random.randint(100, 999),
            "email": "user@enterprise.com",
            "total_sent": 100,
            "total_inbox": 95,
        }
        self.client.post(
            "http://localhost:8001/webhook",
            json=payload,
            name="/smartlead-sync/webhook",
        )

    @task(4)
    def simulate_analytics_ingest(self):
        payload = {
            "account_email": "user@enterprise.com",
            "sent": 100,
            "inbox": 95,
            "spam": 5,
        }
        self.client.post(
            "http://localhost:8003/analytics/ingest",
            json=payload,
            name="/analytics/ingest",
        )

    @task(2)
    def trigger_workflow_readiness(self):
        payload = {
            "campaign_id": f"camp-{random.randint(1000, 9999)}",
            "mailbox_count": 5,
            "avg_inbox_rate": 98.5,
        }
        self.client.post(
            "http://localhost:8004/workflow/start",
            json=payload,
            name="/workflow/start",
        )
