import base64
import datetime
import os
from datetime import date

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, cc_email)

import io
from xlsx2html import xlsx2html
import pandas as pd

# Converting downloaded Daily report to html
def convert_excel_to_html(file_name):
    xlsx_file = open(file_name, 'rb')
    all_dfs = pd.read_excel(file_name, sheet_name=None)
    result_html = ""
    for keys in all_dfs.keys():
       out_file = io.StringIO()
       xlsx2html(xlsx_file, out_file, locale='en', sheet=keys)
       out_file.seek(0)
       result_html += out_file.read() + "<br/>"

    return result_html

def send_mail(message):
    #message.attachment = attachedFile
    #message.add_cc(cc_email)

    sg = SendGridAPIClient(os.environ['API_KEY'])
    response = sg.send(message)
    print(response.status_code, response.body, response.headers)

def prepare_mail(report_txt, report_path, jira_txt, jira_path, id, name, console_op):
    data = '<html><body><h5>Hi All,</h5><p>Please find the attached daily Status report. (You can see details  <b><a ' \
       'href="#">here</a></b>)</p>' + report_txt + \
       '<br/> <br/><p><b>JIRA REPORT:-</b></p>' + jira_txt + '<p>Thanks and Regards</p><p>Name</p></body></html>'
    
    # Sending Email
    #cc_email=''
    today = str(date.today()).split("-")
    if "non2go" in report_path:
        subject = "Status" + " : Enterprise - " + today[2] + "." + today[1]
    elif "2go" in report_path:
        subject = "Status1" + " : Enterprise - " + today[2] + "." + today[1]
    else:
        subject = "Status" + " : " + today[2] + "." + today[1]
    attachment_path_list = [report_path, console_op, jira_path]
    to_emails = [
        (id, name)
    ]

    message = Mail(
        from_email='sender_mail@example.com',
        to_emails=to_emails,
        is_multiple=True,
        subject=subject,
        html_content=data
    )
    if attachment_path_list is not None:
        for each_file_path in attachment_path_list:
            try:
                file_name=each_file_path.split("/")[-1]
                file_path=each_file_path
                with open(file_path, 'rb') as f:
                    data = f.read()
                    f.close()
                encoded_file = base64.b64encode(data).decode()

                attachedFile = Attachment(
                    FileContent(encoded_file),
                    FileName(file_name),
                    FileType('application/xlsx'),
                    Disposition('attachment')
                )
                message.attachment = attachedFile
            except Exception as e:
                print("could not attache file")
                print(e)
    
    send_mail(message)


filename_2go = 'test' + str(datetime.date.today()) + '.xlsx'
filename_non2go = 'test' + str(datetime.date.today()) + '.xlsx'
console_output_2go = 'console' + str(datetime.date.today()) + '.txt'
console_output_non2go = 'console' + str(datetime.date.today()) + '.txt'
jiraname = './jira_' + str(datetime.date.today()) + '.xlsx'


daily_report_result_2go = convert_excel_to_html(filename_2go)
daily_report_result_non2go = convert_excel_to_html(filename_non2go)
jira_report_result = convert_excel_to_html(jiraname)

prepare_mail(daily_report_result_2go, filename_2go, jira_report_result, jiraname, 'test@example.com', 'test', console_output_2go)
prepare_mail(daily_report_result_non2go, filename_non2go, jira_report_result, jiraname, 'test@example.com', 'Test', console_output_non2go)
