# handlers/smart_group_batch_handler.py
import csv
import time
import logging
from sys_rest_controller import SysRestController
from create_smart_group_dto import CreateSmartGroupDTO

# Configure logging
logging.basicConfig(filename="smart_group_handler.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SmartGroupBatchHandler:
    def __init__(self, retry_attempts=3, retry_delay=5):
        self.sys_rest_controller = SysRestController()
        self.smart_group_batch = []
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay

    def load_smart_groups_from_csv(self, file_path):
        """Loads smart groups from a CSV file."""
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.add_smart_group_to_batch(row)
            logging.info(f"Loaded {len(self.smart_group_batch)} smart groups from {file_path}.")
        except Exception as e:
            logging.error(f"Error loading CSV file: {e}")

    def add_smart_group_to_batch(self, group_data):
        """Adds a smart group to the batch."""
        smart_group_dto = CreateSmartGroupDTO(
            group_name=group_data['group_name'],
            description=group_data['description'],
            organization_group_id=group_data['organization_group_id'],
            platform=group_data['platform'],
            criteria_type=group_data['criteria_type']
        )
        self.smart_group_batch.append(smart_group_dto)

    def process_smart_group_batch(self):
        """Processes the batch of smart groups with retry logic."""
        results = []
        for group_dto in self.smart_group_batch:
            for attempt in range(1, self.retry_attempts + 1):
                try:
                    response = self.sys_rest_controller.create_smart_group(group_dto.to_dict())
                    results.append({"group_name": group_dto.group_name, "status": "success", "response": response})
                    logging.info(f"Successfully created smart group: {group_dto.group_name}")
                    break
                except Exception as e:
                    logging.error(f"Error creating smart group {group_dto.group_name}: {e}")
                    if attempt < self.retry_attempts:
                        logging.info(f"Retrying ({attempt}/{self.retry_attempts}) for smart group {group_dto.group_name}...")
                        time.sleep(self.retry_delay)
                    else:
                        results.append({"group_name": group_dto.group_name, "status": "failed", "error": str(e)})
                        logging.error(f"Failed to create smart group {group_dto.group_name} after {self.retry_attempts} attempts.")

        # Clear batch after processing
        self.smart_group_batch.clear()
        return results

# Example usage
if __name__ == "__main__":
    handler = SmartGroupBatchHandler()
    csv_file_path = "smart_groups.csv"  
    handler.load_smart_groups_from_csv(csv_file_path)
    
    # Process the batch with retry and logging
    results = handler.process_smart_group_batch()
    for result in results:
        print(result)