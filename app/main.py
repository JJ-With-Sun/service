from fastapi import FastAPI
import inference
import ppt_maker
import send_email_new
import send_fail_email
import send_email_ppt
import test_qudrant
import linkedin_messaging

app = FastAPI(
    title=f'YSkids InnovaMatch API',
    description='InnovaMatch from YSKids',
)

# inbound
# 평가 -> 입력 : 없음 -> 합불 리스트 6명 (json)
# 합불 메일 전송 -> 입력 : 없음(합불리스트) (리스트 json, 면접 참가자 채점 정보) -> 메일 전송
# PPT 전송 -> 입력 : 없음(합불리스트) (리스트 json, 면접 참가자 채점 정보) -> PPT 전송 (메일)

# outbound
# project 정보 넘겨받아서 -> 크롤링, RAG 결과
# 메일 전송 -> 챗봇

# 챗봇
model = inference.Evaluator()

@app.get('/evaluate/{company}')
async def evaluate(company: str):
    # /home/kic/yskids/service/data/SAMSUNG/2018recrute 폴더에 있는 파일을 읽어서 평가 recruit
    data = model.inference(f"/home/kic/yskids/service/data/{company}")
    return {"message": "Complete!"}



@app.get("/sender/{company}")
async def inbound_sender(company: str):
    path = f"/home/kic/yskids/service/data/{company}"
    data = ppt_maker.create_ppt_from_excel(path)
    send_email_new.send(path)
    send_fail_email.send(path)
    send_email_ppt.send(path)
    return {"message": "Complete!"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to YSKids InnovaMatch API!"}

@app.get("/suggest/{company}/.")
async def outbound_sender(company: str):
    linkedin_messaging.send_message(company)
    return {"message": "Complete!"}

@app.get("/search/{company}")
async def outbound_search(company: str):
    df = test_qudrant.rag(f"/home/kic/yskids/service/data/{company}")
    return {"message": "Complete!"}
    
