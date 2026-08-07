#  This file is part of OctoBot Prediction Market (https://github.com/Drakkar-Software/OctoBot-Prediction-Market)
#  Copyright (c) Drakkar-Software, All rights reserved.

import os
import json
import octobot_prediction_market.cli

# Import your custom OmnibookExchange class
from octobot_prediction_market.exchange_data.exchange import OmnibookExchange


def main():
    # 1. Set default fallback keys
    api_key = "YOUR_OMNIBOOK_API_KEY"
    api_secret = "YOUR_OMNIBOOK_API_SECRET"

    # 2. Read from config/lynx.json
    config_path = "config/lynx.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            omnibook_cfg = config.get("exchanges", {}).get("omnibook", {})
            api_key = omnibook_cfg.get("api-key", api_key)
            api_secret = omnibook_cfg.get("api-secret", api_secret)
    else:
        print(f"⚠️ Warning: '{config_path}' was not found. Using default placeholder keys.")

    # 3. Instantiate your custom exchange client
    exchange = OmnibookExchange(api_key=api_key, api_secret=api_secret)

    # 4. Test the connection
    try:
        if api_key == "YOUR_OMNIBOOK_API_KEY":
            print("⚠️ Warning: API keys are not set in lynx.json. The bot will start but cannot connect to Omnibook yet.")
        else:
            balance = exchange.get_account_balance()
            print(f"Successfully connected to Omnibook! Current Balance: {balance}")
    except Exception as e:
        print(f"Error connecting to Omnibook API: {e}")

    # 5. Start the main OctoBot CLI loop
    octobot_prediction_market.cli.main()


if __name__ == "__main__":
    main()
