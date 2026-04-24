"""
로컬/클라우드 겸용 실행 스크립트.

로컬 : python run.py               -> http://0.0.0.0:8000
Render: PORT 환경변수로 포트 자동 설정
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
