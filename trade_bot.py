import os
import time
import json
from octobot_prediction_market.exchange_data.exchange import OmnibookExchange

def get_keys():
    # Load your keys from lynx.json
    with open("config/lynx.json", "r") as f:
        config = json.load(f)
        omnibook_cfg = config.get("exchanges", {}).get("omnibook", {})
        return omnibook_cfg.get("api-key"), omnibook_cfg.get("api-secret")

def run_strategy():
    api_key, api_secret = get_keys()
    exchange = OmnibookExchange(api_key=api_key, api_secret=api_secret)
    
    print("🤖 Starting AI Trading Bot for Omnibook...")
    
    try:
        balance = exchange.get_account_balance()
        print(f"💰 Starting Balance: {balance}\n")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # --- MAIN TRADING LOOP ---
    while True:
        try:
            print("📊 Fetching market data...")
            # Here is where your AI/Logic will go!
            # For now, let's just make a simple default prediction to test execution.
            direction = "UP"  
            trade_amount = 5.0  # $5 play-money test trade
            
            print(f"🚀 Placing trade: {trade_amount} on {direction}")
            # Uncomment the line below to actually place real trades!
            # response = exchange.place_prediction(direction=direction, amount=trade_amount, symbol="BTC")
            # print(f"✅ Trade successful: {response}")
            
            print("⏳ Waiting 60 seconds for the next round...\n")
            time.sleep(60)
            
        except Exception as e:
            print(f"⚠️ Error during trade loop: {e}")
            time.sleep(10) # Wait a bit before retrying if there's a network error

if __name__ == "__main__":
    run_strategy()
