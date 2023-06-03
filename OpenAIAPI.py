import openai

openai.api_key = ''

messages = [
    {"role": "system", "content": "Create an image. After the image is created short, detailed story of the image."},
]

focusDetailed = "street view"
adjective1 = "Sunny"
adjective2 = "bright"
visualStyle1 = "light tone"
visualStyle2 = "grainy"
artistReference = "Playboi Cardi"
INPUT = "INPUT = 1234 Lomita Ave, Lomita taken with a film camera"
OUTPUT = f"\nOUTPUT = {focusDetailed},{adjective1},{adjective2},{visualStyle1},{visualStyle2},{artistReference}"

message = '''
INPUT = {focus}
OUTPUT = {description} \n ![IMG](https://image.pollinations.ai/prompt/{description})
{description} = {focusDetailed},%20{adjective1},%20{adjective2},%20{visualStyle1},%20{visualStyle2},%20{artistReference}\n''' + INPUT + OUTPUT

if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

reply = chat.choices[0].message.content
#print(reply)
messages.append({"role": "assistant", "content": reply})

replies = reply.replace("](", "__").replace(")", "__").replace("\n", "").split("__")
print(replies[1])
print(replies[2])