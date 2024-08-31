import socket
import json
import os

with open('input.txt', 'r') as file:
    prompts = [line.strip() for line in file.readlines()]

def start_client(client_id, prompts):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 65432))
    output = []

    try:
        for prompt in prompts:
            client.sendall(prompt.encode())

        for _ in range(len(prompts)):
            response = json.loads(client.recv(1024).decode())
            response["ClientID"] = client_id
            if response["Prompt"] not in prompts:
                response["Source"] = "user"
            output.append(response)

        with open(f'output_{client_id}.json', 'w') as json_file:
            json.dump(output, json_file, indent=4)
        
    except Exception as e:
        pass
    
    finally:
        client.close()

if __name__ == "__main__":
    start_client(client_id=1, prompts=prompts[:6])
    start_client(client_id=2, prompts=prompts[6:])
