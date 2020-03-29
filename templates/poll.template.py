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


# Making an API call to get the JWT token

# To use the server validation feature, use the keyword 'ssl_context' in the http reqeust


# ***** PART 2 - QUERY FOR DEVICES  ***** #


# Get MAC data


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
