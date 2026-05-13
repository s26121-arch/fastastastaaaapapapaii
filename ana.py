from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

PATH = "uploads" # 업로드된 파일을 저장할 디렉토리 경로

@asynccontextmanager # https://fastapi.tiangolo.com/advanced/events/
async def lifespan(app: FastAPI):
    if not os.path.exists(PATH): # 업로드 디렉토리가 존재하지 않으면 생성
        os.makedirs(PATH, exist_ok=True) # exist_ok=True는 디렉토리가 이미 존재해도 에러를 발생시키지 않도록 함 https://docs.python.org/3/library/os.html
    yield

app = FastAPI(lifespan=lifespan) # https://fastapi.tiangolo.com/advanced/events/#lifespan-events

@app.post("/upload") # 파일 업로드 엔드포인트
async def upload_file(file: UploadFile = File(...)): # https://fastapi.tiangolo.com/reference/uploadfile/#fastapi.UploadFile--example
    file_location = os.path.join(PATH, file.filename) # 경로 설정
    with open(file_location, "wb") as f: # 파일을 바이너리 쓰기 모드로 열기
        f.write(await file.read()) # 업로드된 파일의 내용을 읽어서 저장
    return {"info": f"파일이 '{file.filename}' 저장되었습니다 ㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎㅎ"} # 업로드된 파일의 이름과 저장 위치를 반환 (나하진선배님존경합니다 - 최고존엄님 후배)

@app.get("/download/{file_name}") # 파일 다운로드 엔드포인트
async def download_file(file_name: str):
    file_location = os.path.join(PATH, file_name) # 다운로드하려는 파일의 경로 설정
    if os.path.exists(file_location): # 파일이 존재하는지 확인
        return FileResponse(path=file_location, filename=file_name, media_type='application/octet-stream') # 파일이 존재하면 FileResponse를 사용하여 파일을 반환 https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse
    else:
        return {"error": "파일이 배송 도중에 약탈 당했습니다. ㅗㅗ"}