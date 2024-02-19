from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
#import config
import smtplib
import os
from dotenv import load_dotenv

dotenv_path = '/home/kic/yskids/service/app/credentials/.env'
load_dotenv(dotenv_path)

# data = {
#     '지원자 성명': ['조재신', '이준린', '이준하', '조영진', '윤태양', '신연주'],
#     '지원한 직무명': ['마케팅 전략기획', '개발자', '영업 담당자', '인사 담당자', '디자이너', '금융 분석가'],
#     '입사 예정일': ['2023-06-15', '2023-06-20', '2023-06-25', '2023-07-01', '2023-07-05', '2023-07-10'],
#     '입사 장소': ['서울', '부산', '대구', '인천', '광주', '대전'],
#     '이메일 주소': ['winia99@naver.com', 'dlwnsfls123@gmail.com', 'junha4304@gmail.com', 'jenni53@naver.com', 'yuntaeyang0629@yonsei.ac.kr', 'shinyeonjoo98@gmail.com']
# }

def send(path):
    data = {
        '지원자 성명': ['신연주'],
        '지원한 직무명': ['마케팅 전략기획'],
        '입사 예정일': ['2024-03-04'],
        '입사 장소': ['서울'],
        '이메일 주소': ['shinyeonjoo98@gmail.com']
    }


    df = pd.DataFrame(data)


    회사명 = 'KPMG Lighthouse Korea'
    리크루터_성명 = '성OO'
    연락처 = '010-1234-1234'
    이메일주소 = 'winia99@kpmg.com'

    # 나머지 코드는 이어집니다.
    for i, r in df.iterrows():
        # 이메일 설정
        sender_email = 'winia99@naver.com'
        receiver_email = r['이메일 주소']
        subject = f'{회사명} 서류평가 합격 안내 및 면접 안내'

        # HTML 형식의 본문 생성
        html_body = f'''
        <html>
        <table>
        <tr>
        <td width="700"
        padding:10px;">
            <div style = "font-family:Noto Sans KR Medium;
                font-size : 12pt;
                font-weight: bold;
                line-height: 90%;
                color:#00ADB5;">
            [{회사명}]<br><br>
            </div>
            
            <div style = "font-family:Noto Sans KR Medium;
                font-size : 24pt;
                font-weight: bold;
                line-height: 90%;
                color:#00ADB5;
            ">
            합격을 축하합니다. <br><br>
            </div>
    
            안녕하세요 {r['지원자 성명']}님,<br><br>
            저희 회사, {회사명}에서 진행한 {r['지원한 직무명']} 지원에 대한 서류 전형 합격을 축하드립니다!<br><br>
            {r['지원한 직무명']}님께서 정성스럽게 작성해주신 자기소개서와 이력서를 보니, 꼭 만나뵙고 싶다는 생각이 들었습니다.<br><br>
            면접 일정은 다음과 같이 예정되어 있습니다:<br><br>
            면접 예정일: {r['입사 예정일']}<br>
            면접 장소: {r['입사 장소']}<br><br>
            입사 전에 몇 가지 준비사항을 안내드리겠습니다:<br><br>
            신분증, 사진 등의 개인 신상정보를 준비해주시기 바랍니다.<br>
            복장은 캐주얼 또는 비즈니스 캐주얼로 입어주시면 됩니다.<br>
            면접과 관련된 추가 정보는 별도로 안내될 예정입니다. 만약 어떠한 질문이나 요청사항이 있다면, 언제든지 연락 주시기 바랍니다.<br><br>
            다시 한번 축하드리며, 면접때 뵙겠습니다!<br><br>
            감사합니다.<br><br>
            좋은 하루 보내세요!<br><br>
            {리크루터_성명}<br>
            {회사명}<br>
            {연락처}<br>
            {이메일주소}<br>
            </div>
        </td>
        </tr>
        </table>
    </html>
        '''

        # MIMEMultipart 객체 생성
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # HTML 형식의 본문 추가
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)

        # 이메일 보내기
        with smtplib.SMTP('smtp.naver.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(os.getenv('EMAIL_ID'), os.getenv('EMAIL_PASSWORD'))
            server.sendmail(sender_email, [receiver_email], msg.as_string())
