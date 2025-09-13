import requests
from prettytable import PrettyTable

# Target URL
TARGET_URL = "http://localhost"

# Attack vectors
payloads = {
    "XSS": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>"
    ],
    "SQLi": [
        "1' OR '1'='1",
        "admin' --",
        "'; DROP TABLE users; --"
    ],
    "LFI": [
        "../../etc/passwd",
        "/etc/passwd"
    ],
    "RCE": [
        "eval(base64_decode('cGF5bG9hZA=='))",
        "`ls -la`"
    ],
    "PHP Injection": [
        "<?php system('ls'); ?>"
    ],
    "Null Byte": [
        "%00"
    ]
}

# Store results
results = []

print(f"Testing {TARGET_URL} with attack vectors...\n")

for attack_type, attacks in payloads.items():
    print(f"=== {attack_type} ===")
    for attack in attacks:
        try:
            response = requests.get(TARGET_URL, params={"input": attack}, timeout=5)
            status = response.status_code
        except Exception as e:
            status = str(e)
        print(f"Payload: {attack}\nStatus: {status}\n")
        results.append({
            "Attack Type": attack_type,
            "Payload": attack,
            "Status": status,
            "Blocked": status == 403
        })

# Print summary table
table = PrettyTable()
table.field_names = ["Attack Type", "Payload", "Status", "Blocked"]
for r in results:
    table.add_row([r["Attack Type"], r["Payload"], r["Status"], r["Blocked"]])

print("\n=== Summary ===")
print(table)
