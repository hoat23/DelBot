
# coding: utf-8
# Developer: Deiner Zapata Silva.
# Date: 10/06/2020
# Description: Descarga archivos (webscraping), según el archivo excel
#########################################################################################
import os
import xlrd
import requests
import logging
from bs4 import BeautifulSoup
#########################################################################################
logger = logging.getLogger('scraping')

def config_logger() :
    #--------------  CONFIG LOG -------------------------------------------------------
    hdlr = logging.FileHandler('tracer.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)
    #-----------------------------------------------------------------------------------

def normalize(s):
    """
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    """
    return s.replace('\n', ' ').replace('\r', '')

def create_file(path) :
    if not os.path.exists(path) :
        os.makedirs(path)

def scraping_osiptel (path, folder_store) : 
    try:
        host = "https://www.osiptel.gob.pe"
        req = requests.get(path)
        soup = BeautifulSoup(req.content, "html5lib")
        path_file = soup.select_one('.descarga:has(a)').a['href']
        name_file = path_file.split('/')[-1]
        link_download = host + path_file

        logger.info("link => {}".format(link_download))
        logger.info("name => {}".format(name_file))

        req_file = requests.get(link_download)

        with open(folder_store + name_file, 'wb') as pdf:
            pdf.write(req_file.content)

        #documentos asociados
        documents = soup.select_one('.documentos')

        if documents is not None :
            list_doc = documents.ul.find_all("li", recursive=False)
            logger.info('Documentos Asociados => {}'.format(len(list_doc)))

            create_file(folder_store + "asoc")
            
            for item in list_doc:
                link = host + item.a['href']
                name_temp = item.a.text
                name_file = link.split('/')[-1]
                logger.info('Link Asoc => {}'.format(link))
                logger.info('Link Name => {}'.format(name_file))
                
                logger.info('Link NameTemp => {}'.format(normalize(name_temp)))
               
                req_file = requests.get(link)
            
                with open(folder_store + "asoc\\" + name_file, 'wb') as pdf :
                    pdf.write(req_file.content)

                f= open(folder_store + "asoc\\" + name_file.replace(".pdf", "") + ".txt","w+")    
                f.write(normalize(name_temp))
                f.close() 

    except Exception as error:
        logger.error(error)


#config logger
config_logger()
path_dir_proyect = "C:/Users/LENOVO/Documents/PythonCode/ProyectoOsiptel/files"
name_excel = "Filtrado_2.xlsx"

data = xlrd.open_workbook("{0}/{1}".format(path_dir_proyect, name_excel))
path_saved_files = "{0}/book23".format(path_dir_proyect)
"""
[book23]
      |_ [CD]
      |_ [GG]
      |_ [PD]
"""

sheet_names = data.sheet_names()
sheet_data = data.sheets()
logging.info("********************************************************************")
logging.info("********************************************************************")
logger.info('Sheet Names => {}'.format(data.sheet_names()))

for item_sheet in sheet_data:
    logger.info('Sheet : {} => Rows : {}'.format(item_sheet.name, item_sheet.nrows))
    for item_row in range(item_sheet.nrows):
        row_value = item_sheet.row(item_row)
        logger.info("***************************** NEW ROW ***********************************")
        logger.info("Row {} => {}".format(item_row, row_value[3].value))

        folder_store = row_value[6].value
        path = row_value[3].value
        dir_folder_store = folder_store
        if folder_store == 'CD' or folder_store == 'GG' or folder_store == 'PD':
            dir_folder_store = path_saved_files+'\\'+folder_store+'\\' + str(item_row)  + "\\"
            create_file(path_saved_files+'\\'+folder_store+'\\' + str(item_row))
        
        scraping_osiptel(path, dir_folder_store)

