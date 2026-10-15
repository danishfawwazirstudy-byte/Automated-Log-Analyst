import csv 
from datetime import datetime, timedelta 
import random

headers = ["timestamp", "user_id", "source_ip", "event_type", "user_agent", "location", "status"]
users = ["hr_admin_01", "hr_staff_02", "emp_john", "emp_sarah", "dev_alex"]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macitosh; Intel Mac OS X 10_15_7)",
    "Python-urllib/3.10 (Automated Script)"
]

logs = []
base_time = datetime(2026, 8, 20, 8, 0, 0)

# 1. Normal Daily Traffic
for i in range(60):
    t = base_time + timedelta(minutes=random.randint(1, 400))
    logs.append([t.isoformat(), random.choice(users), f"192.168.1{random.randint(10, 50)}", "LOGIN", user_agents[0], "Indonesia", "SUCCESS"])

# 2. Simulate Brute Force Attack (Multiple failed attempts from the same IP)
attacker_ip = f"203.0.113.{random.randint(10, 50)}"
for _ in range(15):
    t += timedelta(seconds=random.randint(2, 10))
    logs.append([t.isoformat(), "hr_admin_01", attacker_ip, "LOGIN", user_agents[2], "Unknown", "FAILED"])

t += timedelta(seconds=random.randint(2, 10))
logs.append([t.isoformat(), "hr_admin_01", attacker_ip, "LOGIN", user_agents[2], "Unknown", "SUCCESS"])

# 3. Save generated log data to a CSV file
import csv 
with open("auth_logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(logs)

print(f"successfully generated {len(logs)} log entries to auth_logs.csv")