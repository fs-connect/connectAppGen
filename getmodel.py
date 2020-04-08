import json
import yaml 
import os
import sys
from generator import load_metadata

def getModel(appPath):
    """ Builds the YAML Model out of existing connect App referenced by folder name. """
    
    propFile = os.path.join(appPath, 'property.conf')
    systemFile = os.path.join(appPath, 'system.conf')
    
    try:
        with open(propFile) as json_file:
            pConf = json.load(json_file)
        with open(systemFile) as json_file:
            sConf = json.load(json_file)
        meta = load_metadata('metadata_parsing.yaml')
    except: 
        print("Error while Loading Configurations files...")
        return None 
    
    
    ## yConf is final Object to be converted to YAML. 
    yConf = {}
    
    ## Parse System Config File 
    
    try:
        
        for k in list(sConf.keys()):
            if k in meta['system_main']:
                yConf[k] = sConf[k]

        yConf['panels'] = {}

        for k in list(sConf['panels'][0].keys()):
            if k in meta['system_panel']: 
                yConf['panels'][k] = sConf['panels'][0][k]
            if k in ['fields']:
                yConf['panels']['fields'] = []
                fieldsList = sConf['panels'][0][k]
                for field in fieldsList:
                    if 'field ID' in list(field.keys()):
                        excludeList = ['connect', yConf['name'].lower()]
                        fieldNameList= [x for x in field['field ID'].split('_') if x not in excludeList]
                        yConf['panels']['fields'].append(" ".join(fieldNameList).strip().capitalize())          

        
    except: 
        print("Error in processing System.conf file!")
        return None 
    
    try: 
        ## Parse Property Config File 
        if 'properties' in list(pConf.keys()):
            yConf['properties'] = [] 
            for prop in pConf['properties']:
                obj = {}
                tagName = ""
                if 'tag' in list(prop.keys()):
                    excludeList = ['connect', yConf['name'].lower()]
                    tagNameList= [x for x in prop['tag'].split('_') if x not in excludeList]
                    tagName = " ".join(tagNameList).strip().capitalize()
                    obj[tagName] = {}

                if tagName != "":    
                    for attr in list(prop.keys()):
                        if attr in meta['property']:
                            obj[tagName][attr] = prop[attr]
                        elif attr in meta['propertyObject']:
                            obj[tagName][attr] = prop[attr]['enable']
                        elif attr in meta['propertyLists']:
                            obj[tagName][attr] = []
                            for attrItem in prop[attr]:
                                if attr == 'subfields':
                                    obj[tagName][attr].append(attrItem['tag'])
                                elif attr == 'options':
                                    obj[tagName][attr].append(attrItem['name'])

                    yConf['properties'].append(obj)
    
    except: 
        print("Error in processing Properties in property.conf file!")
        return None 
    
    try: 
        if 'actions' in list(pConf.keys()):
            yConf['actions'] = []
            for action in pConf['actions']:
                excludeList = ['connect', yConf['name'].lower()]
                actionNameList = [x for x in action['name'].split('_') if x not in excludeList]
                actionName = " ".join(actionNameList).strip().capitalize()
                obj = {}
                for k in list(action.keys()):
                    if k in meta['actions']:
                        obj[k] = action[k]
                        if type(action[k]) == type(""):
                        ## Apply fix if value is boolean in string format
                            if action[k].strip() == 'false': 
                                obj[k] = False
                            elif action[k].strip() == 'true':  
                                obj[k] = True
                    elif k.strip() == 'params':
                        obj['params'] = []
                        actionParamsList = action['params']
                        for param in actionParamsList:
                            excludeList = ['connect', 'action', yConf['name'].lower().strip()]
                            paramNameList = [x for x in param['name'].split('_') if x not in excludeList]
                            obj['params'].append(" ".join(paramNameList).strip().capitalize())
                    elif k.strip() == 'undo':
                        obj['undo'] = action[k]


                ## update the Actions with the created object obj
                yConf['actions'].append({actionName: obj})
    
    except: 
        print("Error in processing Actions in property.conf file!")
        return None
    
    try:
        if 'scripts' in list(pConf.keys()):
            yConf['scripts'] = []
            for script in pConf['scripts']:
                scriptName = script['name'].strip('.py').strip()
                if scriptName.find('test')!=-1:
                    yConf['scripts'].append({'Test': {'test': True}})
                elif scriptName.find('resolve')!=-1:
                    yConf['scripts'].append({'Resolve': 'properties'})
                elif scriptName.find('poll')!=-1:
                    yConf['scripts'].append({'Poll':{'discovery': True}})
                else: 
                    excludeList = ['connect', yConf['name'].lower()]
                    scriptNameList = [x for x in scriptName.split('_') if x not in excludeList]
                    finaleScriptName = " ".join(scriptNameList).strip().capitalize()
                    if 'actions' in list(script.keys()):
                        ## currently we support a single Action link - to be enhanced if neededd!
                        action = script['actions'][0]
                        excludeList = ['connect', yConf['name'].lower()]
                        actionNameList = [x for x in action.split('_') if x not in excludeList]
                        actionName = " ".join(actionNameList).strip().capitalize()
                        obj = {"%s"%finaleScriptName: {'action': "%s"%actionName}}
                    if 'is_cancel' in list(script.keys()):
                        obj[finaleScriptName]['is_cancel'] = script['is_cancel']
                    yConf['scripts'].append(obj)  
                    obj = {}
    
    except: 
        print("Error in processing Scripts in property.conf file!")
        return None
    
    try: 
        # default fileName of the output 
        yaml_file = "%s_model.yaml" % yConf['name'].lower()
        i = 1 
        # if file exists, update filename(x) to iterate through the first non-existing filename(x)
        while os.path.exists(yaml_file):
            yaml_file = "%s_model(%s).yaml" % (yConf['name'].lower(), i)
            i+=1

        with open(yaml_file, 'w') as file:
            print("Generating file: %s"%yaml_file)
            yaml.Dumper.ignore_aliases = lambda *args : True
            yamlOutput = yaml.safe_dump(yConf, file, explicit_start=True, default_flow_style=False, \
                              sort_keys=True, indent=2 )
    
    except: 
        print("Error while writing the model YAML file %s!"%yaml_file)
        return None
    
    return yamlOutput

def main():
    """ Main routine for running the getModel from command line: 
            getmodel <folder_name> 
            
        Example: getmodel cylance_1.0.0 
    """
    
    try:
        path = sys.argv[1]
    except:
        print ("Error: Exception Must pass in the connect App folder name.")
    
    if (len(sys.argv) != 2):
        print("Error: Must pass in exactly one argument")
        return  

    if not os.path.exists(path):
        print ("Error: No Such Folder exists!")
        return 
         
    getModel(path) 
    
if __name__ == "__main__":
    
    main()