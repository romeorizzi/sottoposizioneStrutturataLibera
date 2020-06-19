from IPython.core.display import display, HTML, Markdown, clear_output, Javascript
from IPython.display import IFrame
from IPython.display import Image
import sys
import ipywidgets as widgets
import yaml
import re
import markdown
import os
import sys
import nbformat as nbf
from pdf2image import convert_from_path

#create new notebook
nb = nbf.v4.new_notebook()

#set all input cells hidden
nb['metadata'].update({'hide_input':True})

#yaml opening (todo yaml as arg)
file = open(r'../graph/exercise_graph/config_exercise_graph.yaml')
yaml_list = yaml.load(file, Loader=yaml.FullLoader)


#import notebook
impr='''
import ipywidgets as widgets
from IPython.core.display import display, HTML, Markdown, clear_output, Javascript
from module import preview_generator
import time
import ipywidgets as widgets
import os
import sys
from pdf2image import convert_from_path
'''
nb['cells'].append(nbf.v4.new_code_cell(impr,metadata={"init_cell": True,"trusted": True}))

#uploader, uploader callback and widgets with their callbacks
uploader_code= '''
in_fun@ = 0
name@ = ''
def on_value_change@(change):
    global in_fun@
    global name@
    in_fun@ +=1
    pdf_names = []
    if in_fun@==1 or in_fun@ == 2:
        try:
            name@ = change.new['metadata'][0]['name']
        except:
            pass
        try:
            with open('./attachments/'+name@, "wb") as fp:
                fp.write(change.new[name@]['content'])
            nam, ext  = os.path.splitext(name@)
            r_path =os.path.relpath("./attachments/"+name@)
            if ext =='.pdf':
                #st = "./attachments/"+name1
                pages = convert_from_path("./attachments/"+name@, 500)
                j=0
                for page in pages:
                    page.save('./attachments/img_pdf/'+nam+str(j)+'.png', 'PNG')
                    pdf_names.append('./attachments/img_pdf/'+nam+str(j)+'.png')
                    j = j+1
                for im in pdf_names:
                    display(Markdown("![alt text]("+im+")"))
                pdf_names=[]
            elif ext=='.jpg' or ext=='.png':
                display(Markdown("![alt text](./attachments/"+name@+")"))
            #else:
                #display(Javascript('window.alert("Formato non supportato!")'))
        except:
            pass
    elif in_fun@ == 6:
        in_fun@ = 0

def reset_click@(b):
    display(Javascript("""
        var id@ = Jupyter.notebook.get_selected_index();
        IPython.notebook.execute_cells([id@])
        """))
def add_click@(b):
    display(Javascript("""
        var id1 = Jupyter.notebook.get_selected_index();
        IPython.notebook.insert_cell_below('code')
        """))
def md_click@(b):
    display(Javascript("""
        var id1 = Jupyter.notebook.get_selected_index();
        IPython.notebook.insert_cell_below('markdown')
        """))
 
uploader@ = widgets.FileUpload()
uploader@.observe(on_value_change@, uploader@.value)

button@ = widgets.Button(description="Reset")
output@ = widgets.Output()
button@.on_click(reset_click@)

add_cell@ = widgets.Button(description="Add code cell")
output_add@ = widgets.Output()
add_cell@.on_click(add_click@)

add_md@ = widgets.Button(description="Add md cell")
output_md@ = widgets.Output()
add_md@.on_click(md_click@)

#display(uploader@)
widgets.HBox([uploader@,button@,add_cell@,add_md@])
'''
#widget to create rendition
rendition = '''
sys.path.append('/module/')
button = widgets.Button(description="Preview")
output = widgets.Output()

def render_preview(b):
    display(Javascript('IPython.notebook.save_notebook()'))
    preview_generator.os_nb('loader.ipynb')
button.on_click(render_preview)

widgets.HBox([button])
'''

def substitute(s,i):
    new_s=''
    for l in s:
        if l =='@':
            new_s+=i
        else:
            new_s+=l
    return new_s


i = 1
#append new cells to notebook parsing yaml
for e in yaml_list:
    if re.search('exe_*',e):
        #link to exercise notebook Esercizio_n
        html = '<h1 style="color:red;"><a href="../graph/Esercizio_'+str(i)+'.ipynb">Esercizio '+str(i)+'</a></h1>'
        #get exercise and its md file
        ese = yaml_list.get('exe_'+str(i))
        text = ese.get('text')
        for t in text:
            a = open('../graph/'+t, 'r',encoding='utf-8')
            html = html + markdown.markdown(a.read())                 
            a.close()
        nb['cells'].append(nbf.v4.new_markdown_cell(html))
        nb['cells'].append(nbf.v4.new_code_cell(substitute(uploader_code,str(i)),metadata={"init_cell": True,"trusted": True}))
        i = i+1

nb['cells'].append(nbf.v4.new_code_cell(rendition,metadata={"trusted": True,"init_cell": True}))
#write notebook (todo name of notebook as arg)
nbf.write(nb, 'loader.ipynb')
#set notebook trusted
os.system('jupyter trust loader.ipynb')
