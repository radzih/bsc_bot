import asyncio
import json
import logging

import aiohttp

BASE_URL = "https://api.bscscan.com/api"
MAX_REQUEST_RETRIES = 3

logger = logging.getLogger(__name__)


class BaseAdapter:
    def __init__(self, api_key: str, base_url: str = BASE_URL) -> None:
        self.api_key = api_key
        self.session = aiohttp.ClientSession()
        self.base_url = base_url

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: dict | None = None,
        data: dict | None = None,
        request_retries: int = MAX_REQUEST_RETRIES,
    ) -> dict:
        url = self.base_url + path

        params = params or {}
        params["apikey"] = self.api_key

        for _ in range(request_retries):
            logger.debug(f"Requesting {method} {url}")
            async with self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
            ) as response:
                try:
                    response.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    if response.status == 429:
                        logger.debug("Rate limit exceeded, retrying...")
                        retry_after = int(
                            response.headers.get("Retry-After", 1)
                        )
                        await asyncio.sleep(retry_after)

                    raise e
                else:
                    logger.debug(
                        f"Response {response.status} {response.url.path}"
                    )
                    return await response.json()

    async def _get(self, path: str, params: dict | None = None) -> dict:
        return await self._request("GET", path, params=params)

    async def _post(
        self,
        path: str,
        params: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
    ) -> dict:
        return await self._request(
            "POST", path, params=params, data=data, json=json
        )
