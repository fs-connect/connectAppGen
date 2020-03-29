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
# logging.critical("The server url is {}".format(url))

# ***** START - AUTH API CONFIGURATION ***** #


# Making an API call to get the JWT token

# To use the server validation feature, use the keyword 'ssl_context' in the http reqeust

# ***** END - AUTH API CONFIGURATION ***** #

# ***** PART 2 - QUERY FOR DEVICES  ***** #

# For actions, you can specify user inputted parameters that must be defined in the 'property.conf' file. These parameters will take in user input 
# from the CounterACT console and will be available in the 'params' dictionary.
{% for k,v in r.actions_params.items() %}body["{{ k }}"] = params["{{ v }}"] 
{% endfor %}





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