from observ_windows.obs_window import getlist, clearunsaveddata
import requests

async def sendjob():
    # 60분마다 모인 데이터를 서버로 전송하는 역할
    send2server()

def send2server():
    print('send to server')
    lines = getlist()

    # 보낼 데이터가 없으면 바로 종료
    if not lines:
        print('no data to send')
        return False

    url = "http://localhost:3000/api/windows/set"  # 필요하면 엔드포인트를 바꿔 사용하세요.

    payload = {
        "id": "identify",          # 클라이언트를 구분할 식별자(필요 시 변경)
        "count": len(lines),       # data 리스트의 길이
        "data": list(lines),       # 실제 데이터 리스트
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        print(f"sent: {len(lines)} -> status {response.status_code}")

        # 서버가 정상 응답했으므로, unsaved 데이터(.tempfile + 메모리)를 모두 제거
        clearunsaveddata()
        return True
    except requests.RequestException as e:
        print(f"failed to send {len(lines)}: {e}")
        return False