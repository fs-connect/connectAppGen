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



# Making an API call to get the JWT token



# To use the server validation feature, use the keyword 'ssl_context' in the http reqeust


# ***** END - AUTH API CONFIGURATION ***** #



# ***** PART 2 - DELETE USER  ***** #
# Here, the cookie that was set in adding the user is being used. The user id is used to delete the user.
# DELETE_USER_URL = url + "/users/v2/" + params["cookie"]


r = urllib.request.urlopen(request, context=ssl_context)
request_response = r.getcode()
response = {}
if r.getcode() == 200:
	response["succeeded"] = True
else:
	response["succeeded"] = False
	response["troubleshooting"] = "Failed action. Response code: {}".format(r.getcode())