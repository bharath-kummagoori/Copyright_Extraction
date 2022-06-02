This file licenses under GPLv3


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


# -*- coding: utf-8 -*-
"""
Created on Wed May 25 11:13:11 2022

@author: BKUMMAG
"""

import json
import requests
import ssl
import pandas as pd
from pandas.io.json import json_normalize
from pandas import ExcelWriter
from collections import OrderedDict
import xlsxwriter
#writer=ExcelWriter('',engine ='')
class API_Response:
    
    def __init__(self,username,key,url):
        license_id= file1.get("identifier")
        count=0
        row=0
        col=0
        for i in license_id():
            row+=1
            self.req={
                   "group": "licenses",
                   "action": "get_information",
                   "data": {
                           "username": username,
                           "key": key,
                           "license_identifier":i
                           
                                  #"scan_code": scan_code
                           }

                   }
          
            context=ssl.create_default_context()
            der_certs=context.get_ca_certs(binary_form=True)
            pem_certs=[ssl.DER_cert_to_PEM_cert(der) for der in der_certs]
             #print(pem_certs)
            with open('wincacerts.pem', 'w') as outfile:
                for pem in pem_certs:
                    outfile.write(pem + '\n')
            response = requests.post(url,
                                  headers = {'Content-type': 'application/json'},
                                  data=json.dumps(self.req),verify='wincacerts.pem')
            # self.response = json.loads(response.decode("utf-8"))
            self.response=json.loads(response.text)
            res_dict= json.loads(response.text)
            if res_dict['status']=='1':
                if res_dict.get('data') is not False:
                    res_dict.pop('operation')
                    res_dict.pop('status')
                #print(response_data.response.pop('operation'))
              # writer=pd.ExcelWriter("C:\\MYDrive\\update\\BOM_old\\license_info.xlsx", engine ='xlsxwriter')  
                
                    for k,v in res_dict.items():
                        data=[]
                       # print(v['name'])
                        if v["text"]==None:
                       # name= data.append(v["name"])
                           print(v["name"])
                           print(v["identifier"])
                           
                           new_worksheet.write(row, col, v["identifier"])
                           new_worksheet.write(row, col + 1, v["name"])
                           new_worksheet.write(row, col + 2, v["text"])

                        else:
                            count +=1
                            print(v["name"])
                            print(v["identifier"])
                            new_worksheet.write(row, col, v["identifier"])
                            new_worksheet.write(row, col + 1, v["name"])
                            new_worksheet.write(row, col + 2, v["text"])

                    #self.data=data
                   
        print(count)
                        
                    
                        
     
file1 = pd.read_excel("C:\\MYDrive\\test_sources\\license_list.xlsx", 'sheet')
workbook3 = xlsxwriter.Workbook("C:\\MYDrive\\test_sources\\empty_license.xlsx")  
new_worksheet = workbook3.add_worksheet("result")   
bold = workbook3.add_format({'bold': True})
new_worksheet.write("A1", 'Identifier', bold) 
new_worksheet.write("B1", 'Name', bold) 
new_worksheet.write("C1", 'Text', bold)                      
res = API_Response('','','')
workbook3.close()
