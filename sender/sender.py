from observ_windows.obs_window import getlist, clearunsaveddata
import requests
import common.logger as logger

async def sendjob():
    # 60분마다 모인 데이터를 서버로 전송하는 역할
    send2server()

def send2server():
    logger.info(f'send2server()')
    lines = getlist()

    # 보낼 데이터가 없으면 바로 종료
    if not lines: return False

    url = "http://localhost:3000/api/windows/set"  # 필요하면 엔드포인트를 바꿔 사용하세요.

    flag = True

    while True:
        if len(lines) == 0: break
        length = 50 if 50 < len(lines) else len(lines)

        data = lines[:length]
        lines = lines[length:]

        payload = {
            "id": "identify",          # 클라이언트를 구분할 식별자(필요 시 변경)
            "count": len(data),       # data 리스트의 길이
            "data": list(data),       # 실제 데이터 리스트
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
            logger.info(f'sent: {len(data)} -> status {response.status_code}')
            
            # 서버가 정상 응답했으므로, unsaved 데이터(.tempfile + 메모리)를 모두 제거
        except requests.RequestException as e:
            logger.error(f'failed to send {len(data)}: {e}')
            flag = False
            break

    if flag: clearunsaveddata()
    return flag