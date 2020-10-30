from ipywidgets import widgets
from IPython.display import display, HTML

class connectParams: 
    def __init__(self, name, paramType = '', beginParam = 1, defaultParams = 3, maxParams = 10, displayPanel=True):
        """paramType could be: blank (no type), panel, properties"""
        
        self.name = name
        self.paramType = paramType
        self.panelParams = []
        self.panelParamsType = []
        self.panelVForm = widgets.Label(f'Please choose how many {self.name} (Parameters) you want to generate') 
        self.dd = widgets.Dropdown(
                options=[i for i in range(beginParam, maxParams)],
                value=defaultParams,
                description=f'{self.name}: ',
                disabled=False,
            )

        self.btn_gen = widgets.Button(description=f"Gen {self.name}")
        self.btn_gen.on_click(self.on_panel_header_params_click)

        self.panel_header = widgets.HBox([self.dd, self.btn_gen])
        self.panel = widgets.VBox([self.panel_header,self.panelVForm])
        if displayPanel: 
            display(self.panel)
    
    def close(self): 
        pass
    
    def on_panel_header_params_click(self, b):
        if len(self.panelParams) > 0: 
            for p in self.panelParams: 
                p.close()
            self.panelParams = []
        
        if len(self.panelParamsType) >0:
            for p in self.panelParamsType:
                p.close()
            self.panelParamsType = []

        paramCount = self.dd.value

        if paramCount != 0:
            for i in range(paramCount):
                if self.paramType == '':
                    self.panelParams.append(widgets.Text(description=f"param({i+1})", value=''))
                elif self.paramType == 'panel': 
                    text = widgets.Text(description=f"Param({i+1})", value='')
                    option = widgets.Checkbox(
                                value=False,
                                description='Encrypted',
                                disabled=False,
                                indent=False
                            )
                    self.panelParams.append(widgets.HBox([text, option]))
                elif self.paramType == 'properties': 
                    text = widgets.Text(description=f"Property({i+1})", value='')
                    option1 = widgets.Checkbox(
                                value=True,
                                description='Inventory / Assets Portal',
                                disabled=False,
                                indent=False
                            )
                    option2 = widgets.Checkbox(
                                value=True,
                                description='Track changes',
                                disabled=False,
                                indent=False
                            )
                    option3 = widgets.Checkbox(
                                value=False,
                                description='List',
                                disabled=False,
                                indent=False
                            )
                    option4 = widgets.Checkbox(
                                value=False,
                                description='Boolean',
                                disabled=False,
                                indent=False
                            )
                    self.panelParams.append(widgets.HBox([text, option1, option2, option3, option4]))
                    
                elif self.paramType == 'actions': 
                    text1 = widgets.Text(description=f"Action({i+1})", value='', placeholder='i.e. Add User')
                    text2 = widgets.Text(description=f"Cancel({i+1})", value='', placeholder='i.e. Delete User')
                    header = widgets.HBox([text1, text2])
                    params = connectParams('Act. params', paramType='', beginParam=0, maxParams = 6, displayPanel=False)
                    self.actParams = params
                    self.panelParams.append(widgets.VBox([header, params.panel]))
                    
            self.panelVForm.close()
            self.panelVForm = widgets.VBox(self.panelParams)
            display(self.panelVForm)  
