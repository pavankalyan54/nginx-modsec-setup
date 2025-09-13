
# nginx-modsec-setup

📘 Nginx + ModSecurity v3 + OWASP CRS Installation Guide
1. Install dependencies
sudo apt update && sudo apt install -y \
    git g++ flex bison cmake make \
    libtool automake autoconf pkg-config \
    libpcre3 libpcre3-dev libxml2 libxml2-dev \
    libyajl-dev libssl-dev doxygen zlib1g zlib1g-dev

2. Build and install ModSecurity v3 (library)
cd /usr/local/src
git clone --depth 1 https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
git submodule init
git submodule update
./build.sh
./configure
make
sudo make install

3. Build Nginx with ModSecurity connector
cd /usr/local/src
git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git
wget http://nginx.org/download/nginx-1.26.2.tar.gz
tar -xvzf nginx-1.26.2.tar.gz
cd nginx-1.26.2

./configure --with-compat --add-dynamic-module=../ModSecurity-nginx
make modules


Copy module:

sudo mkdir -p /etc/nginx/modules
sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

4. Enable module in Nginx

Edit /etc/nginx/nginx.conf and add at the very top:

load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;

5. Configure ModSecurity
sudo mkdir -p /etc/nginx/modsec
cd /etc/nginx/modsec


Create modsecurity.conf:

# Enable ModSecurity
SecRuleEngine On

# Audit logging
SecAuditEngine On
SecAuditLog /var/log/modsec_audit.log
SecAuditLogFormat JSON
SecAuditLogParts ABIJDEFHZ
SecAuditLogType Serial

# Debug log (optional)
SecDebugLog /var/log/modsec_debug.log
SecDebugLogLevel 0

# Request/Response settings
SecRequestBodyAccess On
SecRequestBodyLimit 13107200
SecRequestBodyNoFilesLimit 131072
SecRequestBodyLimitAction Reject
SecResponseBodyAccess Off

# Load CRS
Include /etc/nginx/modsec/crs/crs-setup.conf
Include /etc/nginx/modsec/crs/rules/*.conf

# Disabled rules (optional)
Include /etc/nginx/modsec/disabled_rules.conf

6. Install OWASP CRS
cd /etc/nginx/modsec
git clone --depth 1 https://github.com/coreruleset/coreruleset crs
mv crs/crs-setup.conf.example crs/crs-setup.conf
touch disabled_rules.conf

7. Enable ModSecurity in Nginx server block

In your nginx.conf or virtual host:

server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:8080;  # your backend service
        modsecurity on;
        modsecurity_rules_file /etc/nginx/modsec/modsecurity.conf;
    }
}

8. Test & restart
sudo nginx -t
sudo systemctl restart nginx

9. Verify ModSecurity

Test rules:

curl -A "sqlmap" http://localhost/ -i
curl "http://localhost/?testparam=<script>" -i
curl "http://localhost/?p=../etc/passwd" -i


Expected: 403 Forbidden.

10. View logs
# Audit logs (JSON if configured)
cat /var/log/modsec_audit.log

# Debug logs
cat /var/log/modsec_debug.log


✅ At this point you have:

Nginx 1.26.2 built with ModSecurity v3 dynamic module

OWASP CRS loaded and active

Requests like SQLi, XSS, LFI blocked with 403 Forbidden

Audit logs stored in /var/log/modsec_audit.log

### post set up testing with pyton script ####

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

