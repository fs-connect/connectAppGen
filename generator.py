import yaml
import json
import sys
import os

from jinja2 import Template
from connect_images_dir_create import generate_path

# Global Variables used in this module
TEMPLATES_FOLDER = 'templates'
__version__ = '1.0.3'

def load_metadata(fileName = 'metadata.yaml'):
    """Loads metadata file fileName - default: <TEMPLATES_FOLDER>/metadata.yaml """
    try:
        filepath = os.path.join(TEMPLATES_FOLDER, fileName)

        if not os.path.isfile(filepath):
            # fileName does not exist in folder TEMPLATES_FOLDER
            print("Error: Unable to find metadata file: %s " %filepath)
            return None

        with open(filepath) as file:
            # The FullLoader parameter handles the conversion from YAML
            metadata = yaml.load(file, Loader=yaml.FullLoader)

            # do basic santiy checks
            for key in ['main', 'panels', 'properties','actions','scripts']:
                if key not in list(metadata.keys()):
                    print("Error: key %s does not exist in metadata keys list: %s"%(key, str(metadata.keys())))
                    return None

            return metadata

        return None
    except:
        print( "Error: Unable to load meta-data File: %s" %filepath)
        return None

def load_connectApp(fileName):
    """Loads Connect App data from file fileName"""
    try:
        if not os.path.isfile(fileName):
            # fileName does not exist in folder TEMPLATES_FOLDER
            print("Error: Unable to find yaml file: %s " %fileName)
            return None

        with open(fileName) as file:
            # The FullLoader parameter handles the conversion from YAML
            connectApp = yaml.load(file, Loader=yaml.FullLoader)

            # do basic santiy checks
            for key in ['name', 'panels', 'properties','actions','scripts']:
                if key not in list(connectApp.keys()):
                    print("Error: key %s does not exist in metadata keys list: %s"%(key, str(connectApp.keys())))
                    return None

            return connectApp

        return None

    except:
        print( "Error: Unable to load Connect App File: %s" %fileName)
        return None

def saveConf(fileName, confDict):
    """Saves Conf Files based on configuration dictionary. Filename to include connect app folder. """
    try:
        if os.path.isfile(fileName):
            os.remove(fileName)

        with open(fileName, 'w') as outfile:
            json.dump(confDict, outfile, indent=4)

        print("Writing Configurations to: %s" % fileName)

        return True
    except:
        print("Error while writing file: %s"% fileName)
        return False


def generateSconf(fileName, output='system.conf', debug=False):
    """ Generates System Configuration file content.
        Input: fileName connectApp Yaml input file.
        Option: output - default is system.conf - saved to <appName>_<version> folder.
                debug - default is False.
        Output: System Config dict and Saves file output (system.conf) to <appName>_<version>.
                deletes existing output (system.conf) file in this folder if found.
                Returns None if operation is not successful. """

    # loading metadata
    metadata = load_metadata()
    if debug and metadata:
        print("loaded metadata file correctly.")

    # loading connectApp Yaml file
    connectApp = load_connectApp(fileName)
    if debug and connectApp:
        print("loaded connectApp file %s correctly."% fileName)

    if not metadata or not connectApp:
        return None

    # sconf: return value
    sconf = {}

    # load main items, and Extend list Items
    mdMain =  metadata['main']
    mdExtend = list(metadata.keys())

    # set main keys - without the extended ones i.e. ['name', 'version', 'author', 'testEnable']
    for key in [x for x in mdMain if x not in mdExtend ]:
        sconf[key] = connectApp[key]

        # print debug information
        if debug:
            print("debug: following key-value added: %s:%s"%(key, connectApp[key]))

    try:
        # lower case the appName - to be used in default naming convention
        appName = sconf['name'].lower()

        # print debug information
        if debug:
            print("debug: appName added: %s"%appName)

        # create panels list of Objects
        sconf['panels'] = []
        sconf['panels'].append({})

        # get panels dict
        panels = connectApp['panels']

        # Support for a Single Panel today
        # to be enhanced in the future.
        for key in list(panels.keys()):
            if key in metadata['panels'] and key != 'fields':
                sconf['panels'][0][key] = panels[key]

        # print debug information
        if debug:
            print("debug: following keys added to panels[0]: %s"%str(list(panels.keys())))

        if debug:
            print("debug: following panel fields will be processed: %s"%str(list(panels['fields'])))

        # fill the fields
        sconf['panels'][0]['fields'] = []

        i=0
        for key in list(panels['fields']):
            field = {}

            if type(key) == type({}):
                k = list(key.keys())[0]
                v = list(key.values())[0]
                field['display'] = k
                field['field ID'] = 'connect_%s_%s' %(appName, k.lower().replace(' ', '_'))
                field['type'] = v
                field['add to column'] = 'false'
                field['show column'] = 'false'
                field['identifier'] = 'true'
                field['tooltip'] = k
                sconf['panels'][0]['fields'].append(field)
                if debug:
                    print("debug: following field will be added to Panel fields: %s"%str(field))

            else:
                field['display'] = key
                field['field ID'] = 'connect_%s_%s' %(appName, key.lower().replace(' ', '_'))
                field['type'] = 'shortString'
                field['mandatory'] = 'true'
                field['add to column'] = 'true'
                if i == 0:
                    field['show column'] = 'true'
                    i+=1
                else:
                    field['show column'] = 'false'
                field['identifier'] = 'true'
                field['tooltip'] = key
                sconf['panels'][0]['fields'].append(field)

                if debug:
                    print("debug: following field will be added to Panel fields: %s"%str(field))

        # add certification validation
        sconf['panels'][0]['fields'].append({'certification validation': True})

        # add focal appliance and proxy options
        sconf['panels'].append({'focal appliance': True,
         'title': 'Assign CounterACT Devices',
         'description': '<html>Select the connecting CounterACT device that will communicate with the targeted %s instance, including requests by other CounterACT devices. Specific CounterACT devices assigned here cannot be assigned to another server elsewhere.<br><br>If you do not assign specific devices, by default, all devices will be assigned to one server. This server becomes known as the Default Server.<html>' % sconf['name'] })

        sconf['panels'].append({'proxy server': True,
         'title': 'Proxy Server',
         'description': '<html>Select a Proxy Server device to manage all communication between CounterACT and %s.</html>'% sconf['name']})

        if debug:
                print("debug: adding default remaining configurations.")

        # add remaining default options
        field = {}
        field['title'] = "%s Options" % sconf['name']
        field['description'] = field['title']
        field['fields'] = [{'host discovery': True,
          'display': 'Discovery Frequency',
          'max': 72,
          'add to column': 'true',
          'show column': 'false',
          'value': 8},
         {'rate limiter': True,
          'display': 'Number of API queries per unit time',
          'unit': 1,
          'min': 1,
          'max': 1000,
          'add to column': 'true',
          'show column': 'false',
          'value': 100}]
        sconf['panels'].append(field)

        # Save config file to connect App Folder
        # generate path based on connect app name + _ + version
        path = "%s_%s"%(sconf['name'].lower() , sconf['version'])

        # if directory does not exist make-dir
        if not os.path.isdir(path):
            os.mkdir(path)

        systemConfigFile = output
        filepath = os.path.join(path, systemConfigFile)

        # save file to folder
        saveConf(filepath, sconf)

        # returns the dict of systems configuration
        return sconf

    except:
        ## Enhancement needed for logging debug information
        print("Error while generating the Systems Configuration.")
        return None


def generatePconf(fileName, output='property.conf', debug=False):
    """ Generates Property Configuration file content.
        Input: fileName connectApp Yaml input file.
        Option: output - default is property.conf - saved to <appName>_<version> folder.
                debug - default is False.
        Output: Property Config dict and Saves file output (property.conf) to <appName>_<version>.
                deletes existing ouput(property.conf) file in this file if found.
                Returns None if operation is not successful. """

    # loading metadata
    metadata = load_metadata()
    if debug and metadata:
        print("loaded metadata file correctly.")

    # loading connectApp Yaml file
    meta_pconf = load_connectApp(fileName)
    if debug and meta_pconf:
        print("loaded connectApp file %s correctly."% fileName)

    if not metadata or not meta_pconf:
        return None

    try:
        pconf = {}
        pconf['name'] = meta_pconf['name']
        appName = pconf['name'].lower()

        # Generate Default Group Name connect_appname_appname
        group = {}
        group['name'] = 'connect_%s_%s' %(appName, appName)
        group['label'] = pconf['name']
        pconf['groups'] = []
        pconf['groups'].append(group)

        # Reading properties
        pconf['properties'] = []

        for propName in meta_pconf['properties']:
            if type(propName) == type(""):
                prop = {}
                prop['tag'] = "connect_%s_%s" %(appName, propName.lower().strip().replace(" ", "_"))
                prop['label'] = "%s %s" %(pconf['name'], propName)
                prop['description'] = "%s %s" %(pconf['name'], propName)
                prop['type'] = 'string'
                prop['group'] = pconf['groups'][0]['name']
                prop['dependencies'] = []
                prop['dependencies'].append({'name': 'mac', 'redo_new': True, 'redo_change': True})
                pconf['properties'].append(prop)

            elif type(propName) == type({}):
                propTag = list(propName.keys())[0]
                prop = {}
                prop['tag'] = "connect_%s_%s" %(appName, propTag.lower().strip().replace(" ", "_"))
                prop['label'] = "%s %s" %(pconf['name'], propTag)
                prop['description'] = prop['label']
                prop['type'] = 'string'
                for subProp in propName[propTag].keys():
                    if subProp == 'options':
                        if type(propName[propTag][subProp]) == type([]):
                            prop['options'] = []
                            for option in propName[propTag][subProp]:
                                subOption = {}
                                subOption['name'] = option
                                subOption['label'] = option
                                prop['options'].append(subOption)
                        else:
                            print("Error: options should have a list of options!")

                    elif subProp == 'track_change':
                        prop['track_change'] = {}
                        prop['track_change']['enable'] = propName[propTag][subProp]
                        prop['track_change']['label'] = "%s %s Changed" % (pconf['name'], propTag)
                        prop['track_change']['description'] = "Track Change property for %s %s" % (pconf['name'], propTag)
                    elif subProp == 'inventory':
                        prop['inventory'] = {}
                        prop['inventory']['enable'] = propName[propTag][subProp]
                        prop['inventory']['description'] = "Inventory of %s %s" % (pconf['name'], propTag)
                    elif subProp == 'subfields':
                        if type(propName[propTag][subProp]) == type([]):
                            prop['subfields'] = []
                            for option in propName[propTag][subProp]:
                                subOption = {}
                                subOption['tag'] = option.lower()
                                subOption['label'] = option
                                subOption['description'] = "%s %s" %(propTag, option)
                                subOption['type'] = 'string'
                                subOption['inventory'] = True
                                prop['subfields'].append(subOption)
                        else:
                            print("Error: subfields should have a list of subfields!")


                    else:
                        prop[subProp] = propName[propTag][subProp]


                prop['group'] = pconf['groups'][0]['name']

                prop['dependencies'] = []
                prop['dependencies'].append({'name': 'mac', 'redo_new': True, 'redo_change': True})

                pconf['properties'].append(prop)

        # Generate Default Action Group Name connect_appname_appname
        group = {}
        group['name'] = 'connect_%s_%s' %(appName, appName)
        group['label'] = pconf['name']
        pconf['action_groups'] = []
        pconf['action_groups'].append(group)

        # Reading Actions
        if 'actions' in list(meta_pconf.keys()):
            pconf['actions'] = []
            for actionItem in meta_pconf['actions']:
                actionName = list(actionItem.keys())[0]
                prop = {}
                prop['name'] = "connect_%s_%s" %(appName, actionName.lower().strip().replace(" ", "_"))
                prop['label'] = actionName
                prop['group'] = pconf['groups'][0]['name']
                for item in list(actionItem[actionName].keys()):
                    if item == 'params':
                        prop[item] = []
                        for param in actionItem[actionName][item]:
                            element = {}
                            element['name'] = "connect_%s_%s" %(appName,param.lower().strip().replace(" ", "_") )
                            element['label'] = param
                            element['description'] = "%s %s" %(appName, param)
                            element['type'] = 'string'
                            prop['params'].append(element)
                    elif item == 'undo':
                        prop['undo'] = {'label':actionItem[actionName][item]['label'],
                                        'description': actionItem[actionName][item]['description']}
                    else:
                        prop[item] = actionItem[actionName][item]

                prop['dependencies'] = [{'name': 'mac', 'redo_new': True, 'redo_change': True}]
                pconf['actions'].append(prop)

        ## Generating Scripts & .py files templates
        scriptNameList = []
        if 'scripts' in list(meta_pconf.keys()):
            pconf['scripts'] = []
            for scriptItem in meta_pconf['scripts']:
                scriptName = list(scriptItem.keys())[0]
                prop = {}
                prop['name'] = "%s_%s.py" %(appName, scriptName.lower().strip().replace(" ", "_"))
                scriptOptions = scriptItem[scriptName]
                if type(scriptOptions) == type(""):
                    if scriptOptions == 'properties':
                        prop['properties'] = []
                        for itemProp in pconf['properties']:
                            if itemProp['tag'].find('policy') == -1:
                                prop['properties'].append(itemProp['tag'])
                elif type(scriptOptions) == type({}):
                    for scriptOption in list(scriptOptions.keys()):
                        if scriptOption.lower().strip() == 'action':
                            prop['actions'] = []
                            prop['actions'].append( "connect_%s_%s" %(appName, \
                                                    scriptOptions[scriptOption].lower().strip().replace(" ", "_")))
                        else:
                            prop[scriptOption] = scriptOptions[scriptOption]

                pconf['scripts'].append(prop)

        ## Generating Policies
        pconf['policy_template'] = {}

        ptg = {}
        ptg['name'] = "connect_%s" %(appName)
        ptg['label'] = pconf['name']
        ptg['display'] = pconf['name']
        ptg['description']= '%s templates' % pconf['name']
        ptg['full_description'] = "<html>Use %s policy templates to manage devices in a %s environment:<ul><li>Detect devices that are compliant.</li></ul></html>" %(pconf['name'], pconf['name'])
        ptg['title_image'] = 'connect_%s.png' % appName
        ptg['bg_image'] = 'bg_%s.png' % appName
        pconf['policy_template']['policy_template_group'] = ptg

        ptp = {}
        ptp['name'] = "connect_%s_compliant" %(appName)
        ptp['label'] = "%s Compliance" % (pconf['name'])
        ptp['display'] = "%s Compliance" %(pconf['name'])
        ptp['help'] = "%s Compliance Policy" % (pconf['name'])
        ptp['description'] = "Creates %s Compliance Policies" % (pconf['name'])
        ptp['file_name'] = '%sCompliance.xml'%(pconf['name'])
        ptp['full_description'] = "<html>Use this policy template to detect corporate hosts that are compliant.</html>"
        ptp['title_image'] = '%s.png' % appName

        pconf['policy_template']['policies'] = [ptp]


        # Save config file to connect App Folder
        # generate path based on connect app name + _ + version
        path = "%s_%s"%(meta_pconf['name'].lower() , meta_pconf['version'])

        # if directory does not exist make-dir
        if not os.path.isdir(path):
            os.mkdir(path)

        propertiesConfigFile = output
        filepath = os.path.join(path, propertiesConfigFile)

        # save file to folder
        saveConf(filepath, pconf)

        return pconf

    except:
        ## Enhancement needed for logging debug information
        print("Error while generating the Properties Configuration.")
        return None

def resolveVariables(fileName):
    """ Internal function -
        Generates Dictionary of parameters / actions_parameters / properties to be used in Python Jinja2 Templates.
        Input: fileName - connectApp Yaml file.
        output: dict of properties / parameters / actions_parameters to be used in Scripts Templates.
        """
    connectApp = load_connectApp(fileName)

    if not connectApp:
        return None

    appName = connectApp['name'].lower().replace(" ", "_").replace("-", "_")

    folder = "%s_%s"%(appName, connectApp['version'])

    resolveVars = {
        'name':appName,
        'folder': folder,
        'propsMap': "%s_to_ct_props_map" % appName,
        'properties': {},
        'params': {},
        'actions_params':{},
        'scripts':[]
    }

    for prop in connectApp['properties']:
        if type(prop) == type({}):
            propKey = list(prop.keys())[0]
            if propKey.lower() != 'policy':
                resolveVars['properties'][propKey.lower().strip().replace(" ", "_")] = "connect_%s_%s" % \
                    (appName, propKey.lower().strip().replace(" ", "_"))

        elif type(prop) == type(""):
            resolveVars['properties'][prop.lower().strip().replace(" ", "_")] = "connect_%s_%s" % \
                    (appName, prop.lower().strip().replace(" ", "_"))

    for param in connectApp['panels']['fields']:
        if type(param) == type(""):
            resolveVars['params'][param.lower().strip().replace(" ", "_")] = "connect_%s_%s" % \
                (appName, param.lower().strip().replace(" ", "_"))
        elif type(param) == type({}):
            k = list(param.keys())[0]
            resolveVars['params'][k.lower().strip().replace(" ", "_")] = "connect_%s_%s" % \
                (appName, k.lower().strip().replace(" ", "_"))


    ## Extract actions_parameters to be used in python Jinja2 templates
    for action in connectApp['actions']:
        for param in action[list(action.keys())[0]]['params']:
            resolveVars['actions_params'][param.lower().strip().replace(" ", "_")] = "%s_%s" % \
            (appName, param.lower().strip().replace(" ", "_"))

    ## Extract template Name to be used <action>.<template>.py while generating the templates
    if 'settings' in list(connectApp.keys()):
        if 'template' in list(connectApp['settings']):
            resolveVars['template'] = connectApp['settings']['template']
        else:
            resolveVars['template'] = 'template'
    else:
        resolveVars['template'] = 'template'


    if 'scripts' in list(connectApp.keys()):
        for script in connectApp['scripts']:
            sName = list(script.keys())[0].lower().strip().replace(" ", "_").replace("-", "_")
            if sName in ['test', 'poll', 'resolve']:
                _scriptName = "%s_%s.py" %(appName, sName)
                _scriptTemplate = "%s.%s.py"%(sName, resolveVars['template'])
                resolveVars['scripts'].append({_scriptName:_scriptTemplate})
            else:
                ## script is an action
                ## detect if action is_cancel or normal action
                ## map it to action.<template>.py
                _scriptName = "%s_%s.py" %(appName, sName)

                scriptOptions = script[list(script.keys())[0]]

                if 'is_cancel' in list(scriptOptions.keys()):
                    _scriptTemplate = "action.cancel.%s.py"%(resolveVars['template'])
                else:
                    _scriptTemplate = "action.%s.py"%(resolveVars['template'])

                resolveVars['scripts'].append({_scriptName:_scriptTemplate})

    return resolveVars

def writePyCode(scriptName, scriptTemplate, resolveVars, debug=False):
    """ Internal Function:
        Used internally by generatePyScripts function:
        Input: scriptName, scriptTemplate and Vars to be used to generate final code.
        Output: it will write scriptName as generated from Jinja2 Render (scriptTemplate + resolveVars) """

    filePath = os.path.join(TEMPLATES_FOLDER, scriptTemplate)

    if not os.path.isfile(filePath):
        print("Error in Code Generation! - Template file (%s) does not exist in %s folder"%(scriptTemplate, TEMPLATES_FOLDER))
        return None

    if not os.path.isdir(resolveVars['folder']):
        os.mkdir(resolveVars['folder'])

    try:
        f = open(filePath, 'r')
        fcontent = f.read()
        f.close()
        tmp = Template(fcontent)
        result = tmp.render(r = resolveVars)
        if result != "":
            dstFilePath = os.path.join(resolveVars['folder'], scriptName)
            if os.path.isfile(dstFilePath):
                if debug:
                    print("Warning: over-writing python file: %s"%dstFilePath)
                os.remove(dstFilePath)

            print("Writing Generated code to %s"%dstFilePath)
            foutput = open(dstFilePath, "w")
            foutput.write(result)
            foutput.close()

        return result

    except:
        print("Error while processing the ScripName: %s, and ScriptTemplate: %s." %(scriptName, scriptTemplate))
        return None

def generatePyScripts(fileName):
    """ Public Function to generate all Python Scripts defined in connectApp Yaml file.
        input: connectApp Yaml File.
        Output: it will generate all Python files needed by the connectApp based on the provided template Name.
        returns True if all is good, otherwise None."""


    resolvedVars = resolveVariables(fileName)
    errors = False

    if not resolvedVars:
        print("Error Generating Python Scripts: - while resolving Variables!")
        return None

    if 'scripts' not in list(resolvedVars.keys()):
        print("Error Generating Python Scripts: - Cannot find the Scripts input!")
        return None

    for script in resolvedVars['scripts']:
        if type(script) != type({}):
            print("Error Generating Python Scripts: - script type is not correct!")
            errors = True
        else:
            scriptName = list(script.keys())[0]
            scriptTemplate = script[scriptName]
            result = writePyCode(scriptName,scriptTemplate, resolvedVars)
            if not result:
                print("Error Generating Python Scripts for ScriptName: %s using Template: %s"%(scriptName,scriptTemplate))
                errors = True

    if not errors:
        print("Scripts successfully generated!")
        return True
    else:
        print("There were some errors while generating scripts!")

    return None



def generateApp(fileName):
    """ Simply combines the three functions: generateSconf, generatePconf and generatePyScripts.
        Input: fileName of connectApp Yaml file.
        Output: Creates main app folder + Configuration files + Python Scripts based on templates.
    """
    systemsConfig = generateSconf(fileName)

    if not systemsConfig:
        print("Halting - faced problem while generating system config file..")
        return None

    propConfig = generatePconf(fileName)
    if not propConfig:
        print("Halting - faced problem while generating property config file..")
        return None

    generatePyScripts(fileName)

    resolvedVars = resolveVariables(fileName)
    propertyFilePath = os.path.join(resolvedVars['folder'], 'property.conf')

    print("Generating Images folders..")
    generate_path(propertyFilePath)

    ## Adding folder for Policies
    ## policies/nptemplates
    policiesFolder = os.path.join(resolvedVars['folder'], 'policies')
    nptemplatesFolder = os.path.join(policiesFolder, 'nptemplates')

    if not os.path.exists(policiesFolder):
        os.mkdir(policiesFolder)
    if not os.path.exists(nptemplatesFolder):
        os.mkdir(nptemplatesFolder)

    return


def main():
    """ Main routine for running the generator from command line:
            generator sample_app1.yaml
    """
    try:
        path = sys.argv[1]
    except:
        print ("Error: Exception Must pass in the property.conf filename")

    if (len(sys.argv) != 2):
        print("Error: Must pass in exactly one argument")
        return

    if not os.path.exists(path):
        print ("Error: No such file")
        return

    generateApp(path)

if __name__ == "__main__":

    main()
