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
workers = 8
worker_class = "gthread"
bind = ":8000"
chdir = "/app"
