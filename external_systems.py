import requests
from flask import current_app

class InventorySystem:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_inventory(self):
        try:
            response = requests.get(f"{self.api_url}/inventory", headers={"Authorization": f"Bearer {self.api_key}"})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            current_app.logger.error(f"Error fetching inventory: {str(e)}")
            return None

    def update_inventory(self, item_id, quantity):
        try:
            response = requests.post(
                f"{self.api_url}/inventory/update",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"item_id": item_id, "quantity": quantity}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            current_app.logger.error(f"Error updating inventory: {str(e)}")
            return None

inventory_system = None

def init_inventory_system(app):
    global inventory_system
    inventory_system = InventorySystem(
        api_url=app.config.get('INVENTORY_API_URL'),
        api_key=app.config.get('INVENTORY_API_KEY')
    )
