import time
import requests
import json
import os
import sys
from datetime import datetime, timedelta

# Configuration
API_URL = "https://security-zsp5.onrender.com/check_payment"
GRACE_PERIOD_DAYS = 7
TRACKING_FILE = "status.json"

def check_payment_status():
    """Hits the API to check payment status."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("payment_status", False)
    except Exception as e:
        # print(f"Error checking payment status: {e}")
        return None  # Handle API issues gracefully

def get_tracking_data():
    """Loads or initializes the tracking file."""
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as file:
            return json.load(file)
    else:
        return {"last_check": None, "status": True}

def save_tracking_data(status):
    """Updates the tracking file."""
    with open(TRACKING_FILE, 'w') as file:
        json.dump({
            "last_check": datetime.now().isoformat(),
            "status": status
        }, file)

def wreck_code():
    """Destroys the script by deleting critical parts."""
    print("Payment not verified. Wrecking the code...")
    with open('vars.txt', 'w') as script_file:
        script_file.write("# Code disabled due to payment issues.")
    time.sleep(30)
    sys.exit("Code has been wrecked due to payment issues.")

def main():
    tracking_data = get_tracking_data()
    last_check_date = tracking_data["last_check"]
    payment_status = tracking_data["status"]

    # Check if payment was recently verified
    if last_check_date:
        last_check_date = datetime.fromisoformat(last_check_date)
        if datetime.now() - last_check_date > timedelta(days=GRACE_PERIOD_DAYS):
            if not payment_status:
                wreck_code()

    # Verify payment status
    new_status = check_payment_status()
    if new_status is None:
        print("\n Pls connect to mobile network")
        time.sleep(30)
        sys.exit()
    else:
        save_tracking_data(new_status)
        if not new_status:
            print("Payment status invalid. Grace period started.")



