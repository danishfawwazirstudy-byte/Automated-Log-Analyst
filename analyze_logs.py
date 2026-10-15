import pandas as pd

df = pd.read_csv("auth_logs.csv", parse_dates=["timestamp"])
df = df.sort_values("timestamp")

THRESHOLD = 5
WINDOW = pd.Timedelta(minutes=10)

print("======================================")
print("   SUSPICIOUS LOGIN ANALYSIS REPORT   ")
print("======================================")

failures = df[df["status"] == "FAILED"]

# 1a. Brute force: banyak gagal pada satu akun dari satu IP
bf_counts = failures.groupby(["source_ip", "user_id"]).size()
suspicious_bf = bf_counts[bf_counts >= THRESHOLD]

print("\n[1] BRUTE FORCE DETECTION:")
print(suspicious_bf if not suspicious_bf.empty else "No brute force detected.")

# 1b. Password spraying: satu IP gagal ke banyak akun berbeda
spray = failures.groupby("source_ip")["user_id"].nunique()
suspicious_spray = spray[spray >= THRESHOLD]

print("\n[1b] PASSWORD SPRAYING DETECTION:")
print(suspicious_spray if not suspicious_spray.empty else "No spraying detected.")

# 2. Kompromi akun: SUCCESS setelah rangkaian gagal (IP + user sama, dalam jendela waktu)
print("\n[2] POSSIBLE ACCOUNT COMPROMISE:")
hits = []
for (ip, user) in suspicious_bf.index:
    f = failures[(failures.source_ip == ip) & (failures.user_id == user)]
    last_fail = f["timestamp"].max()
    s = df[(df.source_ip == ip) & (df.user_id == user) &
           (df.status == "SUCCESS") &
           (df.timestamp > f["timestamp"].min()) &
           (df.timestamp <= last_fail + WINDOW)]
    if not s.empty:
        hits.append(s)

if hits:
    print(pd.concat(hits).drop_duplicates())
else:
    print("No compromised accounts detected.")