"""Smartlead REST API v1 Endpoint Routes."""

from __future__ import annotations


class Routes:
    """Smartlead API v1 Route Constants."""

    CAMPAIGNS = "/campaigns"
    EMAIL_ACCOUNTS = "/email-accounts"

    @staticmethod
    def campaign_details(campaign_id: int) -> str:
        return f"/campaigns/{campaign_id}"

    @staticmethod
    def email_account_details(account_id: int) -> str:
        return f"/email-accounts/{account_id}"

    @staticmethod
    def warmup_status(account_id: int) -> str:
        return f"/email-accounts/{account_id}/warmup"

    @staticmethod
    def warmup_stats(account_id: int) -> str:
        return f"/email-accounts/{account_id}/warmup-stats"

    @staticmethod
    def warmup_pause(account_id: int) -> str:
        return f"/email-accounts/{account_id}/warmup/pause"

    @staticmethod
    def warmup_resume(account_id: int) -> str:
        return f"/email-accounts/{account_id}/warmup/resume"
