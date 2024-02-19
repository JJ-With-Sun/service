from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
#import config
import smtplib
import os
from dotenv import load_dotenv

dotenv_path = '/home/kic/yskids/service/app/credentials/.env'
load_dotenv(dotenv_path)

def send(path):
    data = {
        '지원자 성명': ['조영진'],
        '지원한 직무명': ['마케팅 전략기획'],
        '입사 예정일': ['2023-06-15'],
        '입사 장소': ['서울'],
        '이메일 주소': ['jenni53@naver.com']
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
        subject = f'{회사명} 서류평가 결과 안내'

        # HTML 형식의 본문 생성
        html_body = f'''
        <html>
        <table>
        <tr>
        <td width="700"
        padding:10px;">
            <div style = "font-family:Noto Sans KR Medium;
                font-size : 18pt;
                font-weight: bold;
                line-height: 90%;
                ">
            {회사명} {r['지원한 직무명']} 사원 모집에 관심을 갖고 지원해주셔서 진심으로 감사드립니다 <br><br>
            </div>
            
    
            안녕하세요 {r['지원자 성명']}님,<br><br>
            {회사명} {r['지원한 직무명']} 계열 채용 담당입니다. <br><br>
            금번에 실시한 {회사명} {r['지원한 직무명']} 사원 모집에 관심을 갖고 지원해주셔서 진심으로 감사 드립니다.<br><br>
            서류지원 과정 중 저희가 의도치 않게 불편을 드린 점은 없었는지 여러모로 마음이 쓰입니다.<br><br>
            귀하의 뛰어난 역량과 잠재력에도 불구하고 안타깝게도 서류심사 과정에서 귀하의 합격 소식을 전해드리지 못하게 되었습니다.<br>
            어떠한 말로도 위로를 건넬 수 없으나 귀하가 보여주신 많은 열정과 노력에 대해 이렇게 짧은 글로나마 안타까운 심정을 전합니다.<br><br>
            감히 말씀 드리자면 귀하의 역량이 부족하다는 것은 결코 아니니 서류 발표로 너무 상심하지 않으셨으면 합니다.<br><br>
            아울러 제출해주신 개인정보는 모두 폐기할 것을 약속 드리며, 추후 재지원에 대한 불이익은 없을 것 입니다.<br>
            비록 이번에는 좋은 만남을 이어나갈 수 없게 되었지만, 이후 더욱 성장한 모습으로 다시금 만날 수 있기를 진심으로 바랍니다.<br><br>
            저희 {회사명}도 지속 성장하여 다음 기회에는 더욱 많은 분들을 모실 수 있도록 하겠습니다.<br><br>
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
