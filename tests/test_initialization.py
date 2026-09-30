import asyncio
import os

import pytest
from UnleashClient import AsyncUnleashClient
from UnleashClient.events import BaseEvent, UnleashEventType


class TestInitialization:
    def test_async_client_imported_from_the_package_root_answers_before_initialization(self, tmp_path) -> None:
        client = AsyncUnleashClient(
            url="http://localhost:4242/api",
            app_name="python-sdk-sandbox",
            cache_directory=str(tmp_path),
        )

        assert client.is_enabled("unknown-toggle") is False

    @pytest.mark.skipif(
        condition="UNLEASH_URL" not in os.environ
        or "UNLEASH_API_TOKEN" not in os.environ
        or "UNLEASH_ENVIRONMENT" not in os.environ,
        reason="UNLEASH_URL, UNLEASH_API_TOKEN and UNLEASH_ENVIRONMENT must be set",
    )
    @pytest.mark.asyncio
    async def test_async_client_reads_a_flag_from_the_sandbox_instance(self, tmp_path) -> None:
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

            assert client.is_enabled("ultimate-feature-flag") is True
        finally:
            await client.destroy()

    @pytest.mark.skipif(
        condition="UNLEASH_URL" not in os.environ
        or "UNLEASH_API_TOKEN" not in os.environ
        or "UNLEASH_ENVIRONMENT" not in os.environ,
        reason="UNLEASH_URL, UNLEASH_API_TOKEN and UNLEASH_ENVIRONMENT must be set",
    )
    @pytest.mark.asyncio
    async def test_async_client_eventually_reads_a_flag_without_waiting_for_ready(self, tmp_path) -> None:
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
            enabled = client.is_enabled("ultimate-feature-flag")
            while not enabled and loop.time() < deadline:
                await asyncio.sleep(0.1)
                enabled = client.is_enabled("ultimate-feature-flag")

            assert enabled is True
        finally:
            await client.destroy()
