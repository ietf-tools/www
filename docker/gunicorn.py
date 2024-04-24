import json

accesslog = "-"
errorlog = "-"
access_log_format = json.dumps(
    {
        "remote_host": "%(h)s",
        "remote_logname": "%(l)s",
        "remote_user": "%(u)s",
        "timestamp": "%(t)s",
        "request": "%(r)s",
        "status_code": "%(s)s",
        "response_size": "%(b)s",
        "referrer": "%(f)s",
        "user_agent": "%(a)s",
        "x_forwarded_for": "%({x-forwarded-for}i)s",
    }
)
capture_output = True
forwarded_allow_ips = "*"
secure_scheme_headers = {"X-CLOUDFRONT": "yes"}
workers = 2
worker_class = "gthread"
worker_connections = 5
bind = ":8000"
keep_alive = 75
chdir = "/app"

# Obfuscate the Server header (to the md5sum of "Springload")
import gunicorn
gunicorn.SERVER_SOFTWARE = "04e96149a2f64d6135c82d199ab62122"
