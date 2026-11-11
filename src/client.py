from pyscript import document
from pyscript.ffi import create_proxy
import json
import js

# 우리가 만든 백엔드 서버(server.py) 주소
SERVER_ADDRESS = 'http://localhost:8080/membership_api/'

# --- [HTTP 요청 전송 함수 4총사] ---
async def post_request(url, parameter):
    r = await js.axios.post(url, parameter)
    return [r.data, r.status, r.statusText]

async def get_request(url):
    r = await js.axios.get(url)
    return [r.data, r.status, r.statusText]

async def put_request(url, parameter):
    r = await js.axios.put(url, parameter)
    return [r.data, r.status, r.statusText]

async def delete_request(url):
    r = await js.axios.delete(url)
    return [r.data, r.status, r.statusText]


# --- [버튼 클릭 이벤트 핸들러 4총사] ---

# 1. CREATE 버튼 클릭 시
async def do_create_by_post(evt):
    k = document.getElementById("key_create").value
    v = document.getElementById("value_create").value
    url = SERVER_ADDRESS + str(k)
    content = json.dumps({str(k): str(v)})

    document.getElementById("key_create").value = ''
    document.getElementById("value_create").value = ''

    # TODO 1: post_request(url, content) 함수를 await 로 호출해서 결과를 res 변수에 담으세요! (1줄)
    res = await post_request(url, content)

    display_msg(f"HTTP POST {url} with {content}", f"{res[1]} {res[2]} - {res[0]}")

# 2. READ 버튼 클릭 시
async def do_read_by_get(evt):
    k = document.getElementById("key_read").value
    url = SERVER_ADDRESS + str(k)
    document.getElementById("key_read").value = ''

    # TODO 2: get_request(url) 함수를 await 로 호출해서 결과를 res 변수에 담으세요! (1줄)
    res = await get_request(url)

    display_msg(f"HTTP GET {url}", f"{res[1]} {res[2]} - {res[0]}")

# 3. UPDATE 버튼 클릭 시
async def do_update_by_put(evt):
    k = document.getElementById("key_update").value
    v = document.getElementById("value_update").value
    url = SERVER_ADDRESS + str(k)
    content = json.dumps({str(k): str(v)})

    document.getElementById("key_update").value = ''
    document.getElementById("value_update").value = ''

    # TODO 3: put_request(url, content) 함수를 await 로 호출해서 결과를 res 변수에 담으세요! (1줄)
    res = await put_request(url, content)

    display_msg(f"HTTP PUT {url} with {content}", f"{res[1]} {res[2]} - {res[0]}")

# 4. DELETE 버튼 클릭 시
async def do_delete_by_delete(evt):
    k = document.getElementById("key_delete").value
    url = SERVER_ADDRESS + str(k)
    document.getElementById("key_delete").value = ''

    # TODO 4: delete_request(url) 함수를 await 로 호출해서 결과를 res 변수에 담으세요! (1줄)
    res = await delete_request(url)

    display_msg(f"HTTP DELETE {url}", f"{res[1]} {res[2]} - {res[0]}")


# 화면 아래쪽에 요청/응답 결과 표시
def display_msg(req_text, res_text):
    document.getElementById("out_request").innerText = req_text
    document.getElementById("out_response").innerText = res_text


if __name__ == '__main__':
    # HTML 버튼들과 파이썬 함수들을 연결!
    document.getElementById("submit_create").addEventListener("click", create_proxy(do_create_by_post))
    document.getElementById("submit_read").addEventListener("click", create_proxy(do_read_by_get))
    document.getElementById("submit_update").addEventListener("click", create_proxy(do_update_by_put))
    document.getElementById("submit_delete").addEventListener("click", create_proxy(do_delete_by_delete))

    document.getElementById("program_status_1").innerText = 'Please fill key/value and execute menu :'
    document.getElementById("program_status_2").innerText = 'READY'