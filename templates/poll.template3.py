import jwt  # PyJWT version 1.6.1 as of the time of authoring
import uuid
import time
from time import gmtime, strftime, sleep
from datetime import datetime, timedelta

# Mapping between {{ r.name }}  response fields to CounterACT properties
{{ r.propsMap }} = {
    {% for k,v in r.properties.items() %} "{{ k }}" : "{{ v }}", 
    {% endfor %}
}

# CONFIGURATION
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
# ***** END - AUTH API CONFIGURATION ***** #

# ***** PART 2 - QUERY FOR DEVICES  ***** #
GETMAC_URL = url + "/devices/v2/"
device_headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(jwt_token)}

# Get MAC data
request = urllib.request.Request(GETMAC_URL, headers=device_headers)
r = urllib.request.urlopen(request, context=ssl_context)
request_response = json.loads(r.read())

# For polling, the response dictionary must contain a list called "endpoints", which will contain new endpoint information. Each endpoint
# must have a field named either "mac" or "ip". The endpoint object/dictionary may also have a "properties" field, which contains property information in the format
# {"propert_name": "property_value"}. The full response object, for example would be: 
# {"endpoints": 
#    [
#       {"mac": "001122334455", 
#        "properties": 
#           {"property1": "property_value", "property2": "property_value2"}
#       }
#    ]
#} 
endpoints=[]
for endpoint_data in request_response["page_items"]:
    endpoint = {}
    mac_with_dash = endpoint_data["mac_addresses"][0]
    mac = "".join(mac_with_dash.split("-"))
    endpoint["mac"] = mac
    properties = {}
    for key, value in endpoint_data.items():
        if key in {{ r.propsMap }} and key is not "mac_addresses":
            properties[{{ r.propsMap }}[key]] = value
    endpoint["properties"] = properties
    endpoints.append(endpoint)
response = {}
response["endpoints"] = endpoints