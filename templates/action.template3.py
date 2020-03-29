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

# There are five debug levels for python: critical, error, warning, info, debug, which have values 1-5 respectively.
# A user can control the debug level by setting the plugin debug level.
logging.critical("The server url is {}".format(url))
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

# ***** PART 2 - QUERY FOR DEVICES  ***** #
ADD_USER_URL = url + "/users/v2/"
device_headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(jwt_token)}
body = dict()

# For actions, you can specify user inputted parameters that must be defined in the 'property.conf' file. These parameters will take in user input 
# from the CounterACT console and will be available in the 'params' dictionary.
{% for k,v in r.actions_params.items() %}body["{{ k }}"] = params["{{ v }}"] 
{% endfor %}
body["user_role"] = "00000000-0000-0000-0000-000000000001"
zones = dict()
zone_array = list()
zones["id"] = "0927bf62-83f4-4766-a825-0b5d2e9749d0"
zones["role_type"] = "00000000-0000-0000-0000-000000000002"
zones["role_name"] = "User"
zone_array.append(zones)
body["zones"] = zone_array
json_body = json.dumps(body).encode('utf-8')

request = urllib.request.Request(ADD_USER_URL, headers=device_headers, data=json_body)
r = urllib.request.urlopen(request, context=ssl_context)
response = {}
# For actions, the response object must have a field named "succeeded" to denote if the action suceeded or not. 
# The field "troubleshooting" is optional to display user defined messages in CounterACT for actions. The field 
# "cookie" is available for continuous/cancellable actions to store information for the same action. For this example,
# the cookie stores the id of the user, which will be used to delete the same user when this action is cancelled.
if r.getcode() == 201:
	response["succeeded"] = True
	request_response = json.loads(r.read())
	id = request_response['id']
	logging.debug("The cookie content is {}".format(id))
	response["cookie"] = id
else:
	response["succeeded"] = False
	response["troubleshooting"] = "Failed action. Response code: {}".format(r.getcode())