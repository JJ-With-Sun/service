import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
#import config
import os
from dotenv import load_dotenv

dotenv_path = '/home/kic/yskids/service/app/credentials/.env'
load_dotenv(dotenv_path)

def send(path):
    # 이메일 설정
    sender_email = 'winia99@naver.com'
    receiver_email = 'winia99@naver.com'
    sender = '성OO'
    subject = 'KPMG Lighthouse Korea 사원 합/불합 PPT 보고서'
    body = f'''
    안녕하세요 {sender}님,

    이번 KPMG Lighthouse Korea 신입사원 채용 1차 서류평가 합/불합 PPT 보고서 첨부드립니다.

    감사합니다.

    '''
    # 첨부할 파일 경로
    file_path = path + '/DEMO/report.pptx'
    filename = 'report.pptx' ##이거 이름 붙혀써야함

    # 이메일 객체 생성
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 파일 첨부
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'vnd.ms-powerpoint')  # PPT 파일의 MIME 타입으로 설정합니다.
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part)

    # 이메일 보내기
    with smtplib.SMTP('smtp.naver.com', 587) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_ID'), os.getenv('EMAIL_PASSWORD'))
        server.sendmail(sender_email, receiver_email, msg.as_string())
