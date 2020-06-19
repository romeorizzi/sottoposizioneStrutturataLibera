import os
import time
from urllib.request import urlopen
import nbformat
from traitlets.config import Config
from nbconvert import HTMLExporter
from nbconvert import RSTExporter, NotebookExporter
from IPython.display import Image, HTML, Javascript
from datetime import datetime

def os_nb(nb_name):
    now = datetime.now() # current date and time
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S") 
    hname = date_time+nb_name[:-6]
    os.system("jupyter nbconvert --to html_embed --output='./preview/"+hname+"' --output-dir='./' "+nb_name+" --no-input")
    display(Javascript('window.open("./preview/'+hname+'.html")'))
    
    