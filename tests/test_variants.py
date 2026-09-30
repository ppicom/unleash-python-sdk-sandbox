import asyncio
import os

import pytest
from UnleashClient import AsyncUnleashClient
from UnleashClient.events import BaseEvent, UnleashEventType

CHEESE_VARIANTS = [
    (1, "fondue"),
    (2, "raclette"),
    (3, "planchette"),
]


class TestVariants:
    @pytest.mark.skipif(
        condition="UNLEASH_URL" not in os.environ
        or "UNLEASH_API_TOKEN" not in os.environ
        or "UNLEASH_ENVIRONMENT" not in os.environ,
        reason="UNLEASH_URL, UNLEASH_API_TOKEN and UNLEASH_ENVIRONMENT must be set",
    )
    @pytest.mark.parametrize(argnames=("user_id", "expected_variant"), argvalues=CHEESE_VARIANTS)
    @pytest.mark.asyncio
    async def test_async_client_resolves_each_users_variant_after_ready(
        self, tmp_path, user_id: int, expected_variant: str
    ) -> None:
        ready = asyncio.Event()
        loop = asyncio.get_running_loop()

        def on_event(event: BaseEvent) -> None:
            if event.event_type == UnleashEventType.READY:
                loop.call_soon_threadsafe(ready.set)

        client = AsyncUnleashClient(
            url=os.environ["UNLEASH_URL"],
            app_name="python-sdk-sandbox",
            custom_headers={"Authorization": os.environ["UNLEASH_API_TOKEN"]},
            environment=os.environ["UNLEASH_ENVIRONMENT"],
            cache_directory=str(tmp_path),
            refresh_interval=1,
            event_callback=on_event,
        )
        try:
            await client.initialize_client()
            await asyncio.wait_for(ready.wait(), timeout=10)

            variant = client.get_variant(feature_name="cheese-variants", context={"userId": user_id})

            assert variant["name"] == expected_variant
        finally:
            await client.destroy()

    @pytest.mark.skipif(
        condition="UNLEASH_URL" not in os.environ
        or "UNLEASH_API_TOKEN" not in os.environ
        or "UNLEASH_ENVIRONMENT" not in os.environ,
        reason="UNLEASH_URL, UNLEASH_API_TOKEN and UNLEASH_ENVIRONMENT must be set",
    )
    @pytest.mark.parametrize(argnames=("user_id", "expected_variant"), argvalues=CHEESE_VARIANTS)
    @pytest.mark.asyncio
    async def test_async_client_eventually_resolves_each_users_variant_without_waiting_for_ready(
        self, tmp_path, user_id: int, expected_variant: str
    ) -> None:
        client = AsyncUnleashClient(
            url=os.environ["UNLEASH_URL"],
            app_name="python-sdk-sandbox",
            custom_headers={"Authorization": os.environ["UNLEASH_API_TOKEN"]},
            environment=os.environ["UNLEASH_ENVIRONMENT"],
            cache_directory=str(tmp_path),
            refresh_interval=1,
        )
        try:
            await client.initialize_client()

            loop = asyncio.get_running_loop()
            deadline = loop.time() + 10
            name = client.get_variant(feature_name="cheese-variants", context={"userId": user_id})["name"]
            while name != expected_variant and loop.time() < deadline:
                await asyncio.sleep(0.1)
                name = client.get_variant(feature_name="cheese-variants", context={"userId": user_id})["name"]

            assert name == expected_variant
        finally:
            await client.destroy()
