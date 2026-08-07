#  This file is part of OctoBot Prediction Market (https://github.com/Drakkar-Software/OctoBot-Prediction-Market)
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  OctoBot is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.

import json
import octobot_prediction_market.cli

# Import your custom OmnibookExchange class from your exchange_data folder
from octobot_prediction_market.exchange_data.exchange import OmnibookExchange


def main():
    # 1. Load API credentials from your config file
    with open("config/default_config.json", "r") as f:
        config = json.load(f)

    omnibook_cfg = config.get("exchanges", {}).get("omnibook", {})
    api_key = omnibook_cfg.get("api-key")
    api_secret = omnibook_cfg.get("api-secret")

    # 2. Instantiate your custom exchange client
    exchange = OmnibookExchange(api_key=api_key, api_secret=api_secret)

    # 3. Test the connection
    try:
        balance = exchange.get_account_balance()
        print(f"Successfully connected to Omnibook! Current Balance: {balance}")
    except Exception as e:
        print(f"Error connecting to Omnibook API: {e}")

    # 4. Start the main OctoBot CLI loop
    octobot_prediction_market.cli.main()


if __name__ == "__main__":
    main()
