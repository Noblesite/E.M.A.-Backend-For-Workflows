# handlers/user_batch_handler.py
import csv
from sys_rest_controller import SysRestController
from create_new_basic_user_dto import CreateNewBasicUserDTO

class UserBatchHandler:
    def __init__(self):
        self.sys_rest_controller = SysRestController()
        self.user_batch = []

    def load_users_from_csv(self, file_path):
        """
        Loads user data from a CSV file and adds them to the batch.
        CSV Format: username, email, password, first_name, last_name, organization_group_id
        """
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.add_user_to_batch(row)
            print(f"Loaded {len(self.user_batch)} users from {file_path}.")
        except Exception as e:
            print(f"Error loading CSV file: {e}")

    def add_user_to_batch(self, user_data):
        """
        Adds a user to the batch.
        :param user_data: Dictionary containing user information.
        """
        user_dto = CreateNewBasicUserDTO(
            user_data['username'],
            user_data['email'],
            user_data['password'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['organization_group_id']
        )
        self.user_batch.append(user_dto)

    def process_user_batch(self):
        """
        Processes the batch of users by calling the API via the SysRestController.
        Returns a list of results.
        """
        results = []
        for user_dto in self.user_batch:
            try:
                response = self.sys_rest_controller.create_user(user_dto.to_dict())
                results.append({"user": user_dto.username, "status": "success", "response": response})
            except Exception as e:
                results.append({"user": user_dto.username, "status": "error", "error": str(e)})

        # Clear batch after processing
        self.user_batch.clear()
        return results

# Example usage
if __name__ == "__main__":
    handler = UserBatchHandler()
    csv_file_path = "users.csv"  # Ensure your CSV is in this path
    handler.load_users_from_csv(csv_file_path)
    
    # Process the batch
    results = handler.process_user_batch()
    for result in results:
        print(result)