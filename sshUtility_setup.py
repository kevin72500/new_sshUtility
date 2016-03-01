# -*- coding: utf-8 -*-  
  
from distutils.core import setup   
import py2exe                            
  
includes = ["encodings", "encodings.*"]
data_files = ['newUtilityRecords.txt']
options = {"py2exe":   
            {   "compressed": 1,           
                "optimize": 2,   
                "bundle_files": 1,   
                "includes": includes  
                  
            }   
          }   
  
setup(       
    version = "2.0",   
    description = "sshUtility2.0",
    name = "sshUtility2.0",
    options = options,   
    zipfile=None,  
	data_files = data_files, 
    console=[{"script": "newUtility.py"}]
    )  