import requests
from base64 import b64encode
from .GetRootFolder import GetRootFolder
import json
import os
from time import sleep

class Builder:

    def TemplateUtf8ToBase64(RawText: str) -> str:
        """
        Convert Utf-8 xml-report to base64

        :param RawText: xml-text in utf-8
        :return: ResultBase64Text - xml-text converted to base64

        """
        CorrectRawText = RawText[RawText.find("<"):]
        ResultBase64Text = b64encode(CorrectRawText.encode()).decode()
        return ResultBase64Text

    def CheckStatusOfFile(ReportId: str) -> str:
        """
        Checking Status Of File
        :param ReportId: Id Of report
        :return: (str) status
        """
        ReportLink = f"https://fastreport.cloud/api/rp/v1/Reports/File/{ReportId}"
        ReportStatusResponse = requests.get(url=ReportLink, headers=GetRootFolder.ReportHeaders)
        return ReportStatusResponse.json()['status']

    def Upload(Filename: str, UserId: str, FileContent: str) -> str:
        """
        Upload base64 xml .frx file to a FastReport.Cloud

        :param str Filename: name of file from user
        :param str UserId: id of user
        :param str FileContent: raw file content in utf-8
        :return str: report id
        """

        ReportData = {
            'name': f'{Filename}',
            'content': Builder.TemplateUtf8ToBase64(FileContent)
                }

        ReportUploadLink = f"https://fastreport.cloud/api/rp/v1/Templates/Folder/{GetRootFolder.TemplatesRootFolderId}/File"

        UploadFileResponse = requests.post(url=ReportUploadLink,
                                           headers=GetRootFolder.ReportHeaders,
                                           json=ReportData)

        if UploadFileResponse.status_code == 200:
            # FileStoragePath = "D:\\Python\\test\\test\\dict.txt"

            # if not os.path.exists(FileStoragePath):
            #     NewFileStorage = open(FileStoragePath, "w")
            #     json.dump({}, NewFileStorage)
            #     NewFileStorage.close()

            # with open(FileStoragePath, "r") as LoadFile:
            #     FileStorage = json.load(LoadFile)

            # FileStorage[UploadFileResponse.json()['id']] = UserId

            # with open(FileStoragePath, "w") as DumpFile:
            #     json.dump(FileStorage, DumpFile)

            return UploadFileResponse.json()['id']

        else:
            return False

    def GetListOfFilesInTemplates():
        GetListOfFilesResponse = requests.get(url=f"https://fastreport.cloud/api/rp/v1/Templates/Folder/{GetRootFolder.ReportRootId}/ListFiles?skip=0&take=10",
                                              headers=GetRootFolder.ReportHeaders)
        return GetListOfFilesResponse.json()['files'][len(GetListOfFilesResponse.json()['files']) - 1]['id']

    def BuildReport(Filename: str, ReportId: str, OutputFormat="Pdf") -> str:
        """
        Build reports in FastReports.Cloud

        :param Filename: name of output file
        :param ReportId: if of report generated in GetListOfFilesInTemplates
        :param OutputFormat: default pdf
        :return: id of built report
        """

        OutputData = {"name": Filename + ".frx",
                      "parentFolderId": GetRootFolder.ReportsRootFolderId
                      }

        ExportFileLink = f"https://fastreport.cloud/api/rp/v1/Templates/File/{ReportId}/Prepare"

        ExportFileResponse = requests.post(url=ExportFileLink,
                                           headers=GetRootFolder.ReportHeaders,
                                           json=OutputData)


        while Builder.CheckStatusOfFile(ExportFileResponse.json()['id']).lower() != 'success':
            sleep(1)

        return ExportFileResponse.json()['id']

    def GetRootFolderTemplates():
        return requests.get(url=f"https://fastreport.cloud/api/rp/v1/Reports/Folder/{GetRootFolder.ReportsRootFolderId}/ListFiles?skip=0&take=10",
                            headers=GetRootFolder.ReportHeaders).json()['files'][0]['id']

    def GetExportFolder():
        return GetRootFolder.GetFolderId("https://fastreport.cloud/api/rp/v1/Exports/Root")

    def ExportReport(Filename, Format = 'Pdf'):
        ExportLink = f"https://fastreport.cloud/api/rp/v1/Reports/File/{Builder.GetRootFolderTemplates()}/Export"
        OutputData = {
            "filename": Filename,
            "folderId": Builder.GetExportFolder(),
            "format": Format
        }
        ExportResponse = requests.post(url=ExportLink, headers=GetRootFolder.ReportHeaders, json=OutputData)
        return ExportResponse.json()['id']

    def CheckStatusOfExport(ReportId: str) -> str:
        """

        :param ReportId:
        :return:
        """
        ReportLink = f"https://fastreport.cloud/api/rp/v1/Exports/File/{ReportId}"
        ReportStatusResponse = requests.get(url=ReportLink, headers=GetRootFolder.ReportHeaders)
        while ReportStatusResponse.json()['status'].lower() != "success":
            continue
        return ReportStatusResponse.json()['status']

    def Download(ReportId: str, FilePath: str):
        """

        :param ReportId:
        :return:
        """
        DownloadLink = f"https://fastreport.cloud/download/e/{ReportId}"
        Response = requests.get(DownloadLink, headers = GetRootFolder.ReportHeaders)
        if Response.status_code == 200:
            with open(FilePath, 'wb') as File:
                for Chunk in Response:
                    File.write(Chunk)