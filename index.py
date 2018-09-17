from __future__ import print_function
import httplib2
import os, io, csv
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
#IG
from InstagramAPI import InstagramAPI
#Time
from time import gmtime, strftime

username = "dictador_del_buen_gusto"
password = "Ch$ris%tian1/"
#Paths
TextPath = "Utiles/description.txt"
ImagePath = "Utiles/photo.jpeg"
ExcelPath = "Utiles/excel.csv"
#Parte de Google Drive

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())
def downloadDocuments(file_id, filepath, DocType = 'text/plain'):
    request = drive_service.files().export_media(fileId=file_id,
                                             mimeType= DocType)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())
def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
        return False
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))
            return item['id']
def DownloadPhotoAndDescription(ListaOrden, index = 0, DescriptionContains = 'textoInsta', PhotoContains = 'fotoInsta'):
    Description = searchFile(1, "name contains '%s%s' " %(DescriptionContains, ListaOrden[index][0][0]) )
    Photo = searchFile(1, "name contains '%s%s' " % (PhotoContains, ListaOrden[index][0][0]) )
    if(Description != False and Photo != False ):
        downloadDocuments(Description, TextPath)
        downloadFile(Photo, ImagePath)
    else:
        print("\n\n\nNo se han podido descargar los archivos debido a que no se encontraron, compruebe que tenga todo escrito correctamente \n\n\n")

#Parte de manipulacion de archivos
def HoraDeExcel(ExcPath, ExcelContains = 'excelInsta'):
    Excel = searchFile(1, "name contains '%s' " % ExcelContains)
    downloadDocuments(Excel, ExcPath, 'text/csv')
    Horas = []
    with open(ExcPath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            Horas.append(row) #Horas es una matriz cuyas filas son orden, hora, minuto
            
    return Horas



archivoTexto = open(TextPath, "r")
texto = archivoTexto.read()



class Instagram:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.InstagramAPI1 = InstagramAPI(self.username, self.password)

    def login(self):
        self.InstagramAPI1.login()

    def uploadPhoto(self, photo_path, caption):
        self.InstagramAPI1.uploadPhoto(photo_path, caption)



#DownloadPhotoAndDescription(horas, 1)

#print(strftime("%H:%M"))


def str2list(lista): # ['1, 2, 3'] --> [1, 2, 3]
    listaFinal = []
    for e in lista:
        lista2 = [x.split(",") for x in e]
        listaFinal.append ( [int(x) for x in lista2[0]] )
    return listaFinal

def publicarEnHorario(horas):
    lista = str2list(horas)
    listaHorasMinutos = [[x[1], x[2]] for x in lista]
    listaIndices = [x[0] for x in lista]
    print(listaIndices)
    for i in range(len(listaIndices)):
        if(int(strftime("%H")) == listaHorasMinutos[i][0] and int(strftime("%M")) == listaHorasMinutos[i][1] ):
            print("hola jeje")

horas = HoraDeExcel(ExcelPath)
publicarEnHorario(horas)