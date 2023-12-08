import os
import datetime
import flet as ft
import subprocess
from xml.dom import minidom


output_folder="./output/"

script_string = '''<script>
        var coll = document.getElementsByClassName("collapsible");
        var i;

        for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
            content.style.display = "none";
            } else {
            content.style.display = "block";
            }
        });
        }
        </script>
        </body>
        </html>'''

header_string='''<html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        body,table,td,tr{
        font-family:monospace;
        font-size:14px;
        }
        .tab{
            border-radius: 3px 3px 0px 0px;
            border-left: 1px solid;
            border-right: 1px solid;
            border-top: 1px solid;
            /* margin-bottom: 10px; */
            padding-left: 4px;
            padding-right: 4px;
            padding-top: 2px;
        }
        .container {
            width: 30em;
            overflow-x: auto;
            white-space: nowrap;
        }
            table{
                border-collapse:collapse;
                border: 1px solid;
                border-spacing: inherit;
            }
            td{border: 1px solid;
            padding-left:4px;
            padding-right:4px;
            }
            tr{
                border-collapse:collapse;
            }
        .collapsible {
            background-color: #777;
            color: white;
            cursor: pointer;
            padding: 18px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            
        }

        .active, .collapsible:hover {
            background-color: #555;
            border-left:5px solid DodgerBlue;
            text-shadow: 1px 2px 5px white;
            
        }

        .content {
            padding: 18px;
            display: none;
            overflow: hidden;
            background-color: #f1f1f1;
            overflow-x: auto;
            white-space: nowrap;
        }
        body>h2{
            text-align:center;
            padding:16px;
        }
        </style>
        </head>
        <body>
        <h2>Algo Details</h2>'''

	#print(os.path.basename(filename))


def main(page: ft.Page):
    
    def atdlReader(filename,file_path_name):
        param_header=[]
        params=[]
        #filename=
        print(filename)
        #fname = os.path.basename(filename)
        fname = filename
        extension = str(fname).split('.')
        print(extension[len(extension)-1])
        if extension[len(extension)-1].lower() != "xml":
            status_text.value = ('Expecting an XML file')
            status_text.color = ft.colors.RED
            status_text.update()
            return
        extension.pop()
        fname = "".join(extension)
        x = datetime.datetime.now()
        fname = fname +"_"+str(x.year)+str(x.month)+str(x.day)+"_"+str(x.hour)+str(x.minute)+str(x.second)+".html"
        print(fname)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        fobj = open(output_folder+fname,"w")
        xmldoc = minidom.parse(file_path_name)
        param_header_string=""
        param_val_string=""
        header=header_string

        #print (params)
        fobj.write(header)
        #parse ATDL File
        strategyIdentifierTag = xmldoc.getElementsByTagName('Strategies')[0].attributes['strategyIdentifierTag'].value
        #print strategyIdentifier
        itemlist = xmldoc.getElementsByTagName('Strategy')
        if len(itemlist) <= 0:
            status_text.value = ("Invalid ATDL file!")
            status_text.color = ft.colors.RED
            status_text.update()
            return
        #print(len(itemlist))
        #print(itemlist[0].attributes['name'].value)
        for s in itemlist:
            print("===============================")
            fobj.write('<button class="collapsible">'+s.attributes['name'].value+'</button><div class="content"><br><label class="tab"><strong>Strategy Details ['+strategyIdentifierTag+']</strong></label><table>')
            print("===============================")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            #print("STRATEGY: "+s.attributes['name'].value) #Strategy Name
            #print("UI Rep: "+s.attributes['uiRep'].value)
            for x in range(0, len(s.attributes)):
                #print s.attributes.item(x).name+","+s.attributes.item(x).value
                fobj.write('<tr><td style="background-color:#62b1ff;">'+s.attributes.item(x).name+"</td><td>"+s.attributes.item(x).value+"</td></tr>")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("-------------------------------")
            fobj.write('</table><br><label class="tab"><strong>Parameters</strong></label><table><tr style="background-color:#62b1ff;">'); #<tr>"+param_header_string+"</tr><tr>"+param_val_string+"</tr>")
            paramlist = s.getElementsByTagName('Parameter')
            x
            params=[]
            param_val_string=""
            for param in paramlist:
                for x in range(0, len(param.attributes)):
                    currVal=param.attributes.item(x).name
                    
                    if params.count(currVal) == 0: #inserting only unique values
                        #print params
                        params.append(str(currVal))
                        '''if str(currVal) == "name":
                            params.insert(0,str(currVal))
                        elif str(currVal) == "fixTag":
                            params.insert(1,str(currVal))
                        elif str(currVal) == "use":
                            params.insert(2,str(currVal))
                        else:'''
                        
                        
                        #fobj.write("<td>"+currVal+"</td>")
                        #print param_val_string
            #param_val_string = param_val_string +"<td>"+currVal+"</td>"
            params.remove("name")
            params.insert(0,"name")
            params.remove("fixTag")
            params.insert(1,"fixTag")
            try:
                if (params.index("use") >= 0):
                    params.remove("use")
                    params.insert(2,"use")
            except ValueError:
                print("NO USE TAG")
            params.append("enumID")
            params.append("wireValue")
            fobj.write("<td>")
            #print ("</td><td>".join(params))
            fobj.write("</td><td>".join(params))
            fobj.write("</td></tr>")
            #fobj.write(",".join(param_header)+"\n")
            #fobj.write(",".join(params)+"\n")
            for param in paramlist:
                strat_param=[""]*len(params)
                #print param.childNodes
                #print len(param.attributes)
                #print("----"+param.attributes['name'].value+"---------------------------")
                for x in range(0, len(param.attributes)):
                    #print param.attributes.item(x).name+" "+param.attributes.item(x).value
                    paramindex=params.index(param.attributes.item(x).name)
                    strat_param[paramindex]=param.attributes.item(x).value
                #ENUM pair of parameters
                enumlist = param.getElementsByTagName("EnumPair")
                enumIDString = ""
                wireValueString = ""
                if len(enumlist) > 0:
                    #print "HERE "+param.attributes['name'].value
                    for enum in enumlist:
                        for i in range(0,len(enum.attributes)):
                            if enum.attributes.item(i).name == "enumID":
                                enumIDString = enumIDString + enum.attributes.item(i).value +"<br>"
                            if enum.attributes.item(i).name == "wireValue":
                                wireValueString = wireValueString + enum.attributes.item(i).value +"<br>"
                            #print enum.attributes.item(i).name+" "+enum.attributes.item(i).value
                print("-------------------------------")
                #fobj.write(",".join(strat_param)+"\n")
                strat_param[len(strat_param)-2]=enumIDString
                strat_param[len(strat_param)-1]=wireValueString
                fobj.write("<tr>")
                for val in strat_param:
                    fobj.write("<td>"+val+"</td>")
                fobj.write("</tr>")
            fobj.write('</table><br><label class="tab"><strong>Layout</strong></label>')
            
            print("Moving to controls")
            
            
            #START for Lay Control
            controls=[]
            controlList = s.getElementsByTagName('lay:Control') #fetching all lay:Control tags elements 
            if (len(controlList) <= 0 ):
                controlList = s.getElementsByTagName('Control') #fetching all Control tags elements 
            
            if (len(controlList) > 0 ):
                fobj.write('<table><tr style="background-color:#62b1ff;">')
                for control in controlList:
                    for x in range(0, len(control.attributes)):
                        #print control.attributes.item(x).name+" "+control.attributes.item(x).value
                        currVal=control.attributes.item(x).name
                        if controls.count(currVal) == 0: #inserting only unique values
                            print(controls)
                            controls.append(str(currVal))
                        #fobj.write("<tr><td>"+control.attributes.item(x).name+" "+control.attributes.item(x).value+"</td></tr>")
                controls.remove("parameterRef")
                controls.insert(0,"parameterRef")
                controls.remove("label")
                controls.insert(1,"label")
                controls.remove("ID")
                controls.insert(2,"ID")
                controls.remove("xsi:type")
                controls.insert(3,"xsi:type")
                controls.append("enumID")
                controls.append("uiRep")
                fobj.write("<td>")
                #print ("</td><td>".join(controls))
                fobj.write("</td><td>".join(controls))
                fobj.write("</td></tr>")
                print(controls)
                for control in controlList:
                    control_data=[""]*len(controls)
                    for x in range(0, len(control.attributes)):
                        controlIndex = controls.index(control.attributes.item(x).name)
                        control_data[controlIndex] = control.attributes.item(x).value
                    
                    listItemList = control.getElementsByTagName("lay:ListItem")
                    if (len(listItemList) <= 0):
                        listItemList = control.getElementsByTagName("ListItem")
                    enumIDString = ""
                    uiRepString = ""
                    if len(listItemList) > 0:
                        print("HERE "+control.attributes['parameterRef'].value)
                        for listItem in listItemList:
                            for i in range(0,len(listItem.attributes)):
                                if listItem.attributes.item(i).name == "enumID":
                                    enumIDString = enumIDString + listItem.attributes.item(i).value +"<br>"
                                if listItem.attributes.item(i).name == "uiRep":
                                    uiRepString = uiRepString + listItem.attributes.item(i).value +"<br>"
                                print(listItem.attributes.item(i).name+" "+listItem.attributes.item(i).value)
                    control_data[len(control_data)-2]=enumIDString
                    control_data[len(control_data)-1]=uiRepString
                    fobj.write("<tr><td>")
                    fobj.write("</td><td>".join(control_data))
                    fobj.write("</td></tr>")
                
                fobj.write("</table>")
            fobj.write("<br></div>")
            #TEST END
        fobj.write(script_string)
        fobj.close()
        #pdfkit.from_file("./output/"+fname, "./output/"+fnamepdf)
        scriptpath = os.path.dirname(os.path.abspath( __file__ ))
        out_file_path = os.path.dirname(os.path.abspath(output_folder+fname))
        status_text.value = ("Completed and created file: ")
        status_text.color = ft.colors.GREEN
        status_text.update()

        global open_path
        #open_path = fr'{scriptpath}\output\{fname}'
        open_path =  fr'{out_file_path}\{fname}'
        output_text.value = (open_path)
        output_text.update()

        open_dir_button.text = f"Open {fname}"
        open_dir_button.visible=True
        open_dir_button.update()


        
	
    def pick_files_result(e: ft.FilePickerResultEvent):
        open_dir_buttonvisible=True
        status_text.value= ("")
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()
        status_text.update()
        if e.files:
            status_text.value = ("Processing...")
            status_text.update()
            f = e.files[0]
            #print(f.path, f.name)
            atdlReader(filename=f.name,file_path_name=f.path)
        else:
            print('Cancelled')

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        #page.update()
        mode_btton.selected = not mode_btton.selected
        page.update()

    global open_path
    def open_file_directory():
        print(open_path)
        subprocess.Popen(fr'explorer /select,"{open_path}"')

    page.title = "ATDL File Parser"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # page.theme = ft.Theme(
    # color_scheme=ft.ColorScheme(primary=ft.colors.PURPLE,))
    mode_btton = ft.IconButton(
                icon="dark_mode",
                selected_icon="light_mode",
                style=ft.ButtonStyle(
                    color={"":ft.colors.BLACK,"selected":ft.colors.WHITE}
                ),
                on_click=toggle_theme,
            )

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(
        weight=ft.FontWeight.BOLD,
        italic=True,
    )
    status_text = ft.Text(
        text_align=ft.TextAlign.CENTER,
        width=300,
        weight=ft.FontWeight.BOLD,
    )
    output_text = ft.Text(
        width=400,
        no_wrap=False,
        selectable=True,
    )

    

    open_dir_button = ft.ElevatedButton(
                    "Open output",
                    icon=ft.icons.FOLDER,
                    on_click=lambda _: subprocess.Popen(fr'explorer /select,"{open_path}"')
                )
    
    open_dir_button.visible = False
    
    
    page.overlay.append(pick_files_dialog)

    page.add(

        ft.AppBar(
            title=ft.Text("ATDL File Parser"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=True,
            actions=[mode_btton,]
        ),

        
        ft.Column(
            [
                ft.ElevatedButton(
                    "Select ATDL file:",
                    icon=ft.icons.FILE_OPEN_ROUNDED,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_files,
                status_text,
                output_text,
                open_dir_button
                
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)

