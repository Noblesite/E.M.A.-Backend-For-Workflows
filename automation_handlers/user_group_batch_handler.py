# handlers/user_group_batch_handler.py
import csv
import time
import logging
from sys_rest_controller import SysRestController
from create_user_group_dto import CreateUserGroupDTO

# Configure logging
logging.basicConfig(filename="user_group_handler.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class UserGroupBatchHandler:
    def __init__(self, retry_attempts=3, retry_delay=5):
        self.sys_rest_controller = SysRestController()
        self.user_group_batch = []
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay

    def load_user_groups_from_csv(self, file_path):
        """Loads user groups from a CSV file and adds them to the batch."""
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.add_user_group_to_batch(row)
            logging.info(f"Loaded {len(self.user_group_batch)} user groups from {file_path}.")
        except Exception as e:
            logging.error(f"Error loading CSV file: {e}")

    def add_user_group_to_batch(self, group_data):
        """Adds a user group to the batch."""
        user_group_dto = CreateUserGroupDTO(
            group_data['group_name'],
            group_data['description'],
            group_data['organization_group_id']
        )
        self.user_group_batch.append(user_group_dto)

    def process_user_group_batch(self):
        """Processes the batch of user groups with retry logic."""
        results = []
        for group_dto in self.user_group_batch:
            for attempt in range(1, self.retry_attempts + 1):
                try:
                    response = self.sys_rest_controller.create_user_group(group_dto.to_dict())
                    results.append({"group_name": group_dto.group_name, "status": "success", "response": response})
                    logging.info(f"Successfully created user group: {group_dto.group_name}")
                    break
                except Exception as e:
                    logging.error(f"Error creating user group {group_dto.group_name}: {e}")
                    if attempt < self.retry_attempts:
                        logging.info(f"Retrying ({attempt}/{self.retry_attempts}) for group {group_dto.group_name}...")
                        time.sleep(self.retry_delay)
                    else:
                        results.append({"group_name": group_dto.group_name, "status": "failed", "error": str(e)})
                        logging.error(f"Failed to create user group {group_dto.group_name} after {self.retry_attempts} attempts.")

        # Clear batch after processing
        self.user_group_batch.clear()
        return results

# Example usage
if __name__ == "__main__":
    handler = UserGroupBatchHandler()
    csv_file_path = "user_groups.csv"  
    handler.load_user_groups_from_csv(csv_file_path)
    
    # Process the batch with retry and logging
    results = handler.process_user_group_batch()
    for result in results:
        print(result)