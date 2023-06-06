import os
from datetime import date
import openai
import requests
from datetime import datetime
from GPStoLocation import location_name, location_weather_description, location_temperature
from functionsTest import adjective1Input, adjective2Input, visualStyle1Input, visualStyle2Input, \
    artistReferenceInput

# insert your API KEY from openAI
openai.api_key = ''

# Initializes chat with chatgpt
messages = [
    {"role": "system", "content": "Create an image and generate a detailed, 5 sentence story "
                                  "of the image in first person. But ONLY output your response as an array. With the "
                                  "first index "
                                  "being the link to the image, and the second index being the story.You have to "
                                  "format your "
                                  "response like EXACTLY like this example [image link || story]. Use the || symbols"
                                  "instead of , to separate the index. And there should be a space inbetween the || "
                                  "and the values"},

]

now = datetime.now()


def get_time_of_day(time):
    if time > 19 or time < 4:
        return "Night"
    elif time < 12:
        return "morning"
    elif time == 12:
        return "Noon"
    elif time < 16:
        return "Afternoon"
    else:
        return "Evening"


time_of_day = get_time_of_day(now.hour)
current_time = now.strftime("%H:%M %p")

today = date.today()
formatted_date = today.strftime("%b_%d_%Y")


# the fields used to help create the image
def createMessage(adjective1, adjective2, visualStyle1, visualStyle2, artistReference):
    INPUT = f"INPUT = A {time_of_day} photo taken at {location_name}. The date is {today}."
    OUTPUT = f"\nOUTPUT = street view image of the location,{adjective1},{adjective2},{visualStyle1},{visualStyle2},{artistReference} "
    return INPUT, OUTPUT


User_Message = createMessage(adjective1Input, adjective2Input, visualStyle1Input, visualStyle2Input,
                             artistReferenceInput)

User_Message_INPUT = User_Message[0]
User_Message_OUTPUT = User_Message[1]

# the message sent to chatgpt
message = '''
INPUT = {focus}
OUTPUT = https://image.pollinations.ai/prompt/{description}
{description} = {focusDetailed},%20{adjective1},%20{adjective2},%20{visualStyle1},%20{visualStyle2},%20{artistReference}\n''' + User_Message_INPUT + User_Message_OUTPUT

if message:
    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

reply = chat.choices[0].message.content
print(reply)
messages.append({"role": "assistant", "content": reply})

# in order to split the information in the reply to return the location and the description of the image
replies = reply.replace("[", "").replace(". _", "").replace("']", "").split("||")

Image_url = ""
Image_desc_data = ""
global success
# to verify if the Image_url is in the replies array
try:
    Image_url = replies[0]  ## have to look at replies variable from now on
    if "http" in Image_url:
        Image_desc_data = replies[1]  # have to look at the replies variable from now on
    else:
        print(replies)
        success = False
        exit()
except IndexError:
    print(replies)
    success = False

# delete these variables because we do not need them anymore
del reply
del replies
del messages
del message

# updates the location variable so that we can name the file after the location
location_name = location_name.replace(" ", "_").replace("#", "_").replace("'", "").replace(",", "_").replace(".", "")

# checks to see if the url is valid
try:
    response = requests.get(Image_url)
except requests.exceptions.MissingSchema as e:
    print("Error: Missing schema in the URL.")
    print("Please try again with a new location or with different ")
    success = False
    exit()

# grabs the image as bytes
img_data = requests.get(Image_url).content

Image_file_name = f'{location_name}_{formatted_date}.jpg'
Image_desc_file_name = f'{location_name}_{formatted_date}_desc.txt'

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

success = True

del img_data

# return Image_file_path, Image_desc_data, success
