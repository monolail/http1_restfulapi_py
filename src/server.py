from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

HOST = "localhost"
PORT = 8080

# 서버의 데이터베이스 역할을 할 딕셔너리 (Key: Value 저장소)
db = {}

class RestApiHandler(BaseHTTPRequestHandler):

    # 요청 정보 로그 출력 함수
    def print_request_info(self, action):
        print(f"\n>> [{action}] 요청 수신 ({self.client_address[0]}:{self.client_address[1]})")
        print(f":: Request Line : {self.requestline}")

    # 공통 HTTP 응답 전송 함수 (CORS 헤더 포함)
    def send_api_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Requested-With')
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        if message:
            self.wfile.write(message.encode('utf-8'))

    # 브라우저의 CORS 사전 확인(Preflight) 요청 처리
    def do_OPTIONS(self):
        self.send_api_response(200, "")

    # 1. [CREATE] 데이터 생성 (HTTP POST)
    def do_POST(self):
        self.print_request_info("CREATE - POST")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)  # 예: {"apple": "1000"}

        key = list(data.keys())[0]
        value = data[key]

        # TODO 1: key가 이미 db에 있으면 'CREATE rejected', 없으면 db[key] = value 저장 후 'CREATE accepted' 응답!
        if key in db:
            print(f":: CREATE {key}:{value} rejected (이미 존재함)")
            content = "CREATE rejected"
        else:
            db[key] = value
            print(f":: CREATE {key}:{value} created (현재 DB: {db})")
            content = "CREATE accepted"

        self.send_api_response(200, content)

    # 2. [READ] 데이터 조회 (HTTP GET)
    def do_GET(self):
        self.print_request_info("READ - GET")
        # URL의 맨 마지막 단어 추출 (예: /membership_api/apple -> 'apple')
        key = self.path.split('/')[-1]

        # TODO 2: key가 db에 있으면 값 반환, 없으면 'READ rejected' 응답!
        if key in db:
            print(f":: READ {key}:{db[key]} completed")
            content = f"READ accepted for < {key} : {db[key]} >"
        else:
            print(f":: READ {key} rejected (존재하지 않음)")
            content = "READ rejected"

        self.send_api_response(200, content)

    # 3. [UPDATE] 데이터 수정 (HTTP PUT)
    def do_PUT(self):
        self.print_request_info("UPDATE - PUT")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)

        key = list(data.keys())[0]
        value = data[key]

        # TODO 3: key가 db에 있으면 db[key] = value 로 수정 후 'UPDATE completed', 없으면 'UPDATE rejected' 응답!
        if key in db:
            db[key] = value
            print(f":: UPDATE {key}:{value} completed (현재 DB: {db})")
            content = "UPDATE completed"
        else:
            print(f":: UPDATE {key}:{value} rejected (존재하지 않음)")
            content = "UPDATE rejected"

        self.send_api_response(200, content)

    # 4. [DELETE] 데이터 삭제 (HTTP DELETE)
    def do_DELETE(self):
        self.print_request_info("DELETE - DELETE")
        key = self.path.split('/')[-1]

        # TODO 4: key가 db에 있으면 del db[key] 로 삭제 후 'DELETE accepted', 없으면 'DELETE rejected' 응답!
        if key in db:
            del db[key]
            print(f":: DELETE {key} completed (현재 DB: {db})")
            content = "DELETE accepted"
        else:
            print(f":: DELETE {key} rejected (존재하지 않음)")
            content = "DELETE rejected"

        self.send_api_response(200, content)


if __name__ == "__main__":
    restful_server = ThreadingHTTPServer((HOST, PORT), RestApiHandler)
    print(f">> RESTful API 서버 시작됨: http://{HOST}:{PORT}")
    print(">> 종료하려면 Ctrl+C 를 누르세요.")

    try:
        restful_server.serve_forever()
    except KeyboardInterrupt:
        restful_server.server_close()
        print("\n>> RESTful API 서버 종료됨")