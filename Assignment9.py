# weather chatbot using meta api
# import MetaAI class from meta_ai_api
from meta_ai_api import MetaAI
llm=MetaAI()
place=input("enter place (i.e city with country : ")

instruction=f'''
you are a custom chatbot and you only have to tell the weater of given place  and  tell me weather in proper format

place is {place}
and if user enter anything else
then you have to print you are a weather gpt and you are not able to tell me except weather
'''
response=llm.prompt(instruction)
print(response["message"])