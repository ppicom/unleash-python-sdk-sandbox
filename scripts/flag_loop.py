"""Poll a feature flag every few seconds and print its state."""

import os
import time

from UnleashClient import UnleashClient

FLAG_NAME = os.environ.get("UNLEASH_FLAG", "ultimate-feature-flag")
INTERVAL_SECONDS = 2


def main() -> None:
    client = UnleashClient(
        url=os.environ["UNLEASH_URL"],
        app_name="python-sdk-sandbox",
        custom_headers={"Authorization": os.environ["UNLEASH_API_TOKEN"]},
    )
    client.initialize_client()

    try:
        while True:
            state = "enabled" if client.is_enabled(FLAG_NAME) else "disabled"
            print(f"{FLAG_NAME} is {state}", flush=True)
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        pass
    finally:
        client.destroy()


if __name__ == "__main__":
    main()
