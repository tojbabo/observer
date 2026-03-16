from observ_windows.obs_window import getlist
import requests

async def sendjob():
    send2server()
    pass

def send2server():
    print('send to server')
    lines = getlist()

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
    except requests.RequestException as e:
        print(f"failed to send {len(lines)}: {e}")