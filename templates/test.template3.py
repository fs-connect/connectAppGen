import jwt  # PyJWT version 1.6.1 as of the time of authoring
import uuid
import json
import urllib.request
import time
from time import gmtime, strftime, sleep
from datetime import datetime, timedelta

# CONFIGURATION
# All server configuration fields will be available in the 'params' dictionary.
{% for k,v in r.params.items() %}{{ k }} = params["{{ v }}"] 
{% endfor %}

# Actions Parameters 
{% for k,v in r.actions_params.items() %}{{ k }} = actions_params["{{ v }}"] 
{% endfor %}

# ***** START - AUTH API CONFIGURATION ***** #
timeout = 1800  # 30 minutes from now
now = datetime.utcnow()
timeout_datetime = now + timedelta(seconds=timeout)
epoch_time = int((now - datetime(1970, 1, 1)).total_seconds())
epoch_timeout = int((timeout_datetime - datetime(1970, 1, 1)).total_seconds())
jti_val = str(uuid.uuid4())
claims = {
    "exp": epoch_timeout,
    "iat": epoch_time,
    "iss": "http://cylance.com",
    "sub": application_id,
    "tid": tenant_id,
    "jti": jti_val,
}

encoded = jwt.encode(claims, application_secret, algorithm='HS256')
payload = {"auth_token": encoded.decode("utf-8")}
headers = {"Content-Type": "application/json; charset=utf-8"}

# Making an API call to get the JWT token
request = urllib.request.Request(url + "/auth/v2/token", headers=headers, data=bytes(json.dumps(payload), encoding="utf-8"))

# To use the server validation feature, use the keyword 'ssl_context' in the http reqeust
resp = urllib.request.urlopen(request, context=ssl_context)
response = {}
# Like the action response, the response object must have a "succeeded" field to denote success. It can also optionally have 
# a "result_msg" field to display a custom test result message.
if resp.getcode() == 200:
    response["succeeded"] = True
    response["result_msg"] = "Successfully connected."
else:
    response["succeeded"] = False
    response["result_msg"] = "Could not connect to {{ r.name }} server."