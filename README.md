# Connect App Generator
Starterkit & Generator for eyeExtend Connect Apps.   

This Folder can be either used with your native python deployemnt (after installing requirements file), or better to spawn a docker Container with Jupyter Notebook - which will allow you to Generate and Edit your eyeExtend App via Jupyter Notebook.

## 1. To execute the scripts directly

Install the required modules:

 `pip3 install -r requirements`

Use the command line to generate the Apps, using provided sample Applications (sample_appX.yaml, etc..)

 `python3 generator.py sample_app1.yaml`

A folder with name appName_appVersion will be automatically created (otherwise overrides existing contents) and (system+property).conf and Python scripts will be auto-generated based on your selected template, including creation of folders. Good Practice to keep proper versioning of your apps so new folders will be created for those new versions.

You will be able to extract the Model (Yaml) file from existing Connect Apps by running the following:

`python3 getmodel.py \<App_Main_Folder\>`

A Yaml file will be created based on "appName_model.yaml" with auto-incremental number if a file already exists with same name.

- - - -

## 2. Build & Run your Docker Container

1. Build your own Container after cloning this repo:

`git clone https://github.com/fs-connect/connectAppGen.git`

`docker build -t connectgen .`

2. Simply Run :
  `docker run --name appGen -d -p 8888:8888 connectgen`

 Then browse to http://docker-machine-ip:8888/ (if local machine use: localhost:8888).

3. Open the Notebook: ConnectAppGen - and execute the cells.

You will then be able to browse through the auto-generated applications accordingly.

## 3. Sample Applications

 Three built-in sample Apps are provided part of this project:

1. sample_app1.yaml => contains dummy XYZ integration, which you can simply tune to help you bootstrap your App. This app uses "template" as Python Scripts template.  
2. sample_app2.yaml => Minimal Slack App (working). Demonstrate the easiest "Hello World!" App by simply posting to Slack via Bot-id, on a default or custom slack channel. This app uses "template2" as Python Scripts template.
3. sample_app3.yaml => More complex - fully featured (workable) Cylance App clone. This app uses "template3" as Python Scripts template.

You can choose any of the above projects to bootstrap your new Connect App Project - simply by modifying the corresponding YAML file and generating the new configurations / Python scrips from the respective templates. We will be covering adding more templates in the next section.

## 4. Selecting / Creating New Python Scripts Templates

In the Settings of the YAML input file, you can define the template name, which will be extracted from default templates folder. You need to define:
  * (poll/resolve/test).templateName.py
  * action.templateName.py        => Same Action template will be applied to all Actions defined in the Model.
  * action.cancel.templateName.py => Same Action Cancelation template will be applied to all undo actions defined in the Model.

Jinja2 is used to define how properties / parameters / actions parameters are used in the python templates to render the generated python code files for the App.

## 5. YAML Connect App File Description

```
name: appName                     => Application Name (Mandatory)
version: 1.0.0                    => Version (Mandatory)
author: Concert Masters           => Author (Mandatory)
testEnable: true                  => testEnable Settings (Mandatory)
panels:                           => Only one Panel is allowed.
    title: appName Connection     => Title to be shown on Top of the Panel
    description: appName Connection => Description
    fields:                       => Panel fields (which will be imported later to Scripts)
        - URL                     => example  
        - Bot Name                
        - Default Channel         
properties:                       => Properties - with or without options. Please refer to eyeExtend Connect documentation.  
    - property1                   => Property name
    - property2
    - property3
actions:                          => List of Actions  
    - Post:                       => Action Name (can contain spaces)
        description: Post New Command => Description
        ip_required: false        => Options
        threshold_percentage: 1
        params:                   => Actions Parameters which will be displayed in the Action dialog box.  
            - Channel
            - Command
scripts:                          => Name of Scripts to be generated for this project
    - Resolve: properties         => Resolve / test / Poll to be fixed if needed - you might remove them if not noeeded.
    - Test:
        test: true
    - Poll:
        discovery: true
    - Post:                       => Script Action to be linked with one of the above actions
        action: Post
    - Delete Post:                => Script CancelAction to be linked with one of the above actions
        action: Post
        is_cancel: true           => important to identify its a Cancelation Script  
settings:
    logoFileName: logo.png        => Not used right now - combining other scripts to generate Logos  
    template: templateX           => Template Name to be used for this Application.
                                     script_type.templateX.py should exists in templates folder.
```

### Revisions

   - rev 1.0.0: eyeExtend Connect App Generator - YAML => (app_folder, property/system.conf files and Python Scripts)  
   - rev 1.0.1: Merging connect-images-dir Script (https://github.com/fs-connect/connect-images-dir).
                The script uses the generated property.conf to generate images folders structure + icons which could be then easily replaced afterwards.
   - rev 1.0.2: Added getmodel.py Script - which reads existing Connect App Main folder -
                (where system/property.conf file exists) and auto-generates the YAML model of the App.
   - rev 1.0.3: Added M3SP connectApp Development Notebook. Added Support to "encrypted" Panel field type.


### Known Limitations

 1. Single Panel is supported in Yaml file
 2. With getmodel.py - Panel Properties' attributes are discarded while creating the Yaml Model, and only certain Attributes with Main Properties are interpreted at this stage.   
