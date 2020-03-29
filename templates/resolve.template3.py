import jwt  # PyJWT version 1.6.1 as of the time of authoring
import uuid
import time
from time import gmtime, strftime, sleep
from datetime import datetime, timedelta


# Mapping between {{ r.name }} response fields to CounterACT properties
{{ r.propsMap }} = {
    {% for k,v in r.properties.items() %} "{{ k }}" : "{{ v }}", 
    {% endfor %}
}

# CONFIGURATION
# All server configuration fields will be available in the 'params' dictionary.
{% for k,v in r.params.items() %}{{ k }} = params["{{ v }}"] 
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

# For properties and actions defined in the 'property.conf' file, CounterACT properties can be added as dependencies. These values will be
# found in the params dictionary if CounterACT was able to resolve the properties. If not, they will not be found in the params dictionary.
if "mac" in params:
    mac = '-'.join(params["mac"][i:i+2] for i in range(0,12,2))
    GETMAC_URL = url + "/devices/v2/macaddress/" + mac
    device_headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(jwt_token)}

    # Get MAC data
    request = urllib.request.Request(GETMAC_URL, headers=device_headers)
    r = urllib.request.urlopen(request, context=ssl_context)
    request_response = json.loads(r.read())

    # All responses from scripts must contain the JSON object 'response'. Host property resolve scripts will need to populate a
    # 'properties' JSON object within the JSON object 'response'. The 'properties' object will be a key, value mapping between the
    # CounterACT property name and the value of the property.
    response = {}
    properties = {}
    if request_response:
        return_values = request_response[0]
        for key, value in return_values.items():
            if key in {{ r.propsMap }}:
                properties[{{ r.propsMap }}[key]] = value

    response["properties"] = properties
else:
    response = {}
    response["error"] = "No mac address to query the endpoint for."