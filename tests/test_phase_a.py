import requests

BASE_URL = "http://localhost:8000"

def verify_task(task_description, expected_output_path, expected_content):
    response = requests.post(f"{BASE_URL}/run", params={"task": task_description})
    assert response.status_code == 200, f"Task failed: {task_description}"

    result = requests.get(f"{BASE_URL}/read", params={"path": expected_output_path})
    assert result.status_code == 200, f"File not found: {expected_output_path}"
    assert result.text.strip() == expected_content, f"Unexpected content in {expected_output_path}"

# Example usage for A3 task verification (Count Wednesdays)
verify_task("Count Wednesdays in /data/dates.txt", "/data/dates-wednesdays.txt", "5")
