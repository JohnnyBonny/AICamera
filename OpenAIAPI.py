import os
from datetime import date
import openai
import requests

# insert your API KEY from openAI
openai.api_key = ''

# Initializes chat with chatgpt
messages = [
    {"role": "system", "content": "Create an image. After the image is created short, detailed story of the image."},
]

# the fields used to help create the image
location = "Torrance Beach,Torrance, CA 90277"
INPUT = f"INPUT = {location} taken with a film camera"  # What you want the image to show

objects1 = ""    #add the input to the focusDetailed variable to include certain objects
objects2 = ""

focusDetailed = "street view"  # a more detailed info of the image
adjective1 = "Sunny"
adjective2 = "bright"
visualStyle1 = "Warm tone"
visualStyle2 = "grainy"
artistReference = "The Weeknd"
OUTPUT = f"\nOUTPUT = {focusDetailed},{adjective1},{adjective2},{visualStyle1},{visualStyle2},{artistReference}"

# the message sent to chatgpt
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
# print(reply)
messages.append({"role": "assistant", "content": reply})

# in order to split the information in the reply to return the location and the description of the image
replies = reply.replace("](", "__").replace(")", "__").replace("\n", "").split("__")

Image_url = ""
Image_desc_data = ""

# to verify if the Image_url is in the replies array
try:
    Image_url = replies[1]
    if "http" in Image_url:
        Image_desc_data = replies[2]
    else:
        print(reply)
        exit()
except IndexError:
    print(reply)

# delete these variables because we do not need them anymore
del reply
del replies
del messages
del message

# updates the location variable so that we can name the file after the location
location = location.replace(" ", "_").replace("#", "_").replace("'", "").replace(",", "_").replace(".", "")

# checks to see if the url is valid
try:
    response = requests.get(Image_url)
except requests.exceptions.MissingSchema as e:
    print("Error: Missing schema in the URL.")
    print("Please try again with a new location or with different ")
    exit()

# grabs the image as bytes
img_data = requests.get(Image_url).content

today = date.today()
formatted_date = today.strftime("%b_%d_%Y")

Image_file_name = f'{location}_{formatted_date}.jpg'
Image_desc_file_name = f'{location}_{formatted_date}_desc.txt'

# creates the path to store the files
directory = "OutputFiles"
Image_file_path = os.path.join(os.getcwd(), directory, Image_file_name)
Image_file_desc_path = os.path.join(os.getcwd(), directory, Image_desc_file_name)

# if the file is there, overwrite. If not, create the file
with open(Image_file_path, 'wb') as handler:
    handler.write(img_data)
    handler.close()

with open(Image_file_desc_path, 'w') as handler:
    handler.write(Image_desc_data)
    handler.close()

#return file_name, Image_desc