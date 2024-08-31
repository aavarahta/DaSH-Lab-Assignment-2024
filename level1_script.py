import os
import time
import json
from groq import Groq

#setting the api key
client = Groq(
    api_key="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"
)

# reading prompts from the file and removing extra whitespaces
with open('input.txt', 'r') as file:
    prompts = [line.strip() for line in file.readlines()]

output = []

# processing each prompt (groq api code)
for prompt in prompts:
    time_sent = int(time.time())  # Record the time the prompt is sent
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    time_recvd = int(time.time())  # recording timestamp

    #appending to the output file
    output.append({
        "Prompt": prompt,
        "Message": chat_completion.choices[0].message.content,
        "TimeSent": time_sent,
        "TimeRecvd": time_recvd,
        "Source": "Groq",
    })

# converting output to json format
with open('output.json', 'w') as json_file:
    json.dump(output, json_file, indent=4)

print("Responses saved to output.json.")
