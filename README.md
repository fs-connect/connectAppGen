# FS Connect App Generator
Starterkit & Generator for eyeExtend Connect Apps.   

This Folder can be either used with your native python deployemnt (after installing requirements file), or better to spawn a docker Container with Jupyter Notebook - which will allow you to Generate and Edit your eyeExtend App via Jupyter Notebook.

## 1. Build and your Docker Container & Run the ConnectAppGen Notebook

a. Build your own Container:
`docker build -t connectGen .`

b. Simply Run :
  `docker run --name appGen -d -p 8888:8888 connectGen`

 Then browse to http://docker-machine-ip:8888/ (if local machine use: localhost:8888).

c. Open the Notebook: ConnectAppGen - and execute the cells.

You will then be able to browse through the auto-generated applications accordingly.

## 2. if you want to execute the scripts directly

Install the required modules:
`pip3 install -r requirements`

Use the command line to generate the Apps, using provided sample Applications (sample_appX.yaml, etc..)

 `python3 generator.py sample_app1.yaml`


### Known Limitations

 1. Single Panel is supported in Yaml file (to be enhanced in the future)
 
