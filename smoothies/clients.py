from __future__ import annotations

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class FruityviceClient:
    """Thin HTTP client for the Fruityvice public API.

    Responsible only for fetching fruit data; aggregation / business logic
    lives in the service layer (SRP).
    """

    BASE_URL = "https://www.fruityvice.com/api/fruit"
    DEFAULT_TIMEOUT = 5

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()

    def get_fruit(self, fruit_name: str) -> Optional[dict]:
        """Return the fruit payload, or ``None`` if the fruit is unknown.

        A response with HTTP 404 (or any network failure) yields ``None`` so
        callers can simply skip the ingredient and continue calculation,
        per the task requirements.
        """
        url = f"{self.base_url}/{fruit_name}"
        try:
            response = self._session.get(url, timeout=self.timeout)
        except requests.RequestException as exc:
            logger.warning("Fruityvice request failed for %r: %s", fruit_name, exc)
            return None

        if response.status_code == 404:
            return None

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            logger.warning(
                "Fruityvice returned %s for %r: %s",
                response.status_code,
                fruit_name,
                exc,
            )
            return None

        try:
            return response.json()
        except ValueError:
            logger.warning("Fruityvice returned non-JSON body for %r", fruit_name)
            return None
