from meta_ai_api import MetaAI
llm=MetaAI()
place=input("Enter the place(i.e city with country  ): ")
instruction=f''''
you are a custom weather bot. 
you have to tell the weather of the place entered by the user.
the ouput should be in proper format
the place is {place}
if user enter something else then ou have to tell that you are a custom weather bot.  you can ask for the place again.
'''
response=llm.prompt(instruction)
print(response["message"]) 