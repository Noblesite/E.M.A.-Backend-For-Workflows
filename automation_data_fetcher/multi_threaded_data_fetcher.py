import concurrent.futures
import json
from mdm_rest_controller import MDMRestController
from sys_rest_controller import SYSRestController
from mam_rest_controller import MAMRestController
from chromadb import Client
from chromadb.config import Settings
from uuid import uuid4

class MultiThreadedDataFetcher:
    def __init__(self, mdm_controller, sys_controller, mam_controller):
        self.mdm_controller = mdm_controller
        self.sys_controller = sys_controller
        self.mam_controller = mam_controller
        self.chroma_client = Client(Settings(persist_directory="./chroma_db"))
        self.collection = self.chroma_client.get_or_create_collection(name="airwatch_data")

    def fetch_organization_groups(self):
        response = self.sys_controller.get_children_organization_groups_from_parent("1")
        return response

    def fetch_devices(self):
        response = self.mdm_controller.get_device_health_check("1", 100, 1)
        return response

    def fetch_applications(self):
        response = self.mam_controller.search_application_by_bundle_id("")
        return response

    def fetch_users(self):
        response = self.sys_controller.search_for_enrollment_user("")
        return response

    def fetch_smart_groups(self):
        response = self.mdm_controller.get_product_info("1")
        return response

    def fetch_user_groups(self):
        response = self.sys_controller.search_custom_user_group_with_params("")
        return response

    def run_parallel_fetch(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.fetch_organization_groups): "Organization Groups",
                executor.submit(self.fetch_devices): "Devices",
                executor.submit(self.fetch_applications): "Applications",
                executor.submit(self.fetch_users): "Users",
                executor.submit(self.fetch_smart_groups): "Smart Groups",
                executor.submit(self.fetch_user_groups): "User Groups"
            }

            results = {}
            for future in concurrent.futures.as_completed(futures):
                category = futures[future]
                try:
                    data = future.result()
                    results[category] = data
                    self.save_to_chromadb(data, category)
                except Exception as e:
                    print(f"{category} generated an exception: {e}")
        return results

    def save_to_chromadb(self, data, category):
        """Save structured data to ChromaDB."""
        for item in data:
            self.collection.add(
                ids=[str(uuid4())],
                documents=[json.dumps(item)],
                metadatas={"category": category}
            )

    def export_to_jsonl(self, data):
        """Convert the data to JSONL format for LLM fine-tuning."""
        jsonl_file_path = "./llm_training_data.jsonl"
        with open(jsonl_file_path, 'w') as jsonl_file:
            for category, records in data.items():
                for record in records:
                    json.dump({"prompt": f"Fetch data for {category}", "response": record}, jsonl_file)
                    jsonl_file.write("\n")
        print(f"LLM training data exported to {jsonl_file_path}")

# Example Usage
mdm_controller = MDMRestController(apiurl="https://api.airwatch.com", tenant="your-tenant", authorization="Bearer Token")
sys_controller = SYSRestController(apiurl="https://api.airwatch.com", tenant="your-tenant", authorization="Bearer Token")
mam_controller = MAMRestController(apiurl="https://api.airwatch.com", tenant="your-tenant", authorization="Bearer Token")

data_fetcher = MultiThreadedDataFetcher(mdm_controller, sys_controller, mam_controller)
results = data_fetcher.run_parallel_fetch()

# Export for LLM training
data_fetcher.export_to_jsonl(results)