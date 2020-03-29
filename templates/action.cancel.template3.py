import jwt  # PyJWT version 1.6.1 as of the time of authoring
import uuid
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

jwt_token = json.loads(resp.read())['access_token']  # access_token to be passed to GET request
# ***** END - AUTH API CONFIGURATION ***** #

# ***** PART 2 - DELETE USER  ***** #
# Here, the cookie that was set in adding the user is being used. The user id is used to delete the user.
DELETE_USER_URL = url + "/users/v2/" + params["cookie"]
device_headers = {"Authorization": "Bearer " + str(jwt_token)}
request = urllib.request.Request(DELETE_USER_URL, headers=device_headers, method='DELETE')
r = urllib.request.urlopen(request, context=ssl_context)
request_response = r.getcode()
response = {}
if r.getcode() == 200:
	response["succeeded"] = True
else:
	response["succeeded"] = False
	response["troubleshooting"] = "Failed action. Response code: {}".format(r.getcode())