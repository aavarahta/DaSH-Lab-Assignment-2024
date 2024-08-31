import socket
import threading
import json
import time
from groq import Groq

client = Groq(
    api_key="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"
)

def handle_client(conn, addr, clients, client_id):
    while True:
        try:
            prompt = conn.recv(1024).decode()
            if not prompt:
                break

            time_sent = int(time.time())  

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
            )
            time_recvd = int(time.time())  

            response = {
                "Prompt": prompt,
                "Message": chat_completion.choices[0].message.content,
                "TimeSent": time_sent,
                "TimeRecvd": time_recvd,
                "Source": "Groq",
                "ClientID": client_id,
            }

            for client_conn in clients:
                client_conn.sendall(json.dumps(response).encode())

        except Exception as e:
            break

    conn.close()
    clients.remove(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 65432))
    server.listen()
    clients = []
    client_id = 0

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        client_id += 1
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients, client_id))
        thread.start()

if __name__ == "__main__":
    start_server()
