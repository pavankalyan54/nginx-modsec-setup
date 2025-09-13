# nginx-modsec-setup

## ⚙️ Dependencies & Setup Notes

These are the exact dependencies and fixes we used to get **Nginx + ModSecurity (with OWASP CRS)** working properly.

### 🔑 System Dependencies
Make sure these are installed:
```bash
sudo apt update
sudo apt install -y nginx libnginx-mod-security2 git curl wget python3 python3-venv python3-pip jq

## ⚙️ Dependencies & Setup Notes

These are the exact dependencies and fixes we used to get **Nginx + ModSecurity (with OWASP CRS)** working properly.

### 🔑 System Dependencies
Make sure these are installed:
```bash
sudo apt update
sudo apt install -y nginx libnginx-mod-security2 git curl wget python3 python3-venv python3-pip jq

load_module modules/ngx_http_modsecurity_module.so;

http {
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsec/main.conf;
}

🛠️ Common Issues & Fixes

Duplicate Rule IDs (934011, etc.)
→ We had the same CRS rule included multiple times.
✅ Fixed by keeping only:

REQUEST-934-APPLICATION-ATTACK-GENERIC.conf

nd removing duplicates like REQUEST-934-APPLICATION-ATTACK-NODEJS.conf.

nginx: [emerg] "modsecurity_rules_file" directive Rule id: XXXX is duplicated
→ Caused by loading the same CRS twice.
✅ Fixed by cleaning nginx.conf to include only one ModSecurity config (main.conf).

pip install failed with “externally-managed-environment”
→ Debian blocked system pip installs.
✅ Fixed by creating a virtual environment for Python:

python3 -m venv venv
source venv/bin/activate
pip install requests

✅ Final Working Steps

To redeploy on a new server:

# 1. Install dependencies
sudo apt update
sudo apt install -y nginx libnginx-mod-security2 git curl wget python3 python3-venv python3-pip jq

# 2. Clone repo
git clone https://github.com/pavankalyan54/nginx-modsec-setup.git
cd nginx-modsec-setup

# 3. Deploy configs
sudo ./setup.sh

# 4. Test & restart nginx
sudo nginx -t
sudo systemctl restart nginx

After this, WAF is active and logs are available at:

/var/log/nginx/access.log

/var/log/nginx/error.log

/var/log/modsec_audit.log

---

👉 This way, next time you just `apt install` dependencies → `git clone` repo → `./setup.sh`. No manual debugging.  

Do you want me to also **add the Python attack test script** into this repo so it becomes part of your standard setup?

