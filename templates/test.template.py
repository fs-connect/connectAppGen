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

# Mapping between {{ r.name }} response fields to CounterACT properties
{{ r.propsMap }} = {
    {% for k,v in r.properties.items() %} "{{ k }}" : "{{ v }}",
    {% endfor %}
}
# ***** START - AUTH API CONFIGURATION ***** #

# Making an API call to get the JWT token

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
