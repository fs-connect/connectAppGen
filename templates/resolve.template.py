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


# Making an API call to get the JWT token

# To use the server validation feature, use the keyword 'ssl_context' in the http reqeust


# For properties and actions defined in the 'property.conf' file, CounterACT properties can be added as dependencies. 
# These values will be found in the params dictionary if CounterACT was able to resolve the properties. 
# If not, they will not be found in the params dictionary.
