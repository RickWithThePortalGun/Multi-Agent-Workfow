import autogen
config_list=[{
    'model':"",
    # Put model and api key here
    'api_key':""
}]

llm_config={
    "request_timeout":600,
    "seed":42,
    "temperature": 0,
    "config_list":config_list
}
llm_config_writer={
    "request_timeout":600,
    "seed":30,
    "temperature": 0.7,
    "config_list":config_list
}

llm_config_examiner={
    "request_timeout":600,
    "seed":22,
    "temperature": 0.5,
    "config_list":config_list
}

researcher=autogen.ConversableAgent(name="Researcher", llm_config=llm_config, system_message="You are a researcher and part of a trio that work on creating questions out of a subject, your role is to develop ideas for teaching someone new to a subject")
writer=autogen.ConversableAgent(name="Writer", llm_config=llm_config_writer, system_message="You are a writer and part of a trio that work on creating questions out of a given subject, your role is to researchers idea to write a piece of text to explain what you recieve.")
examiner=autogen.ConversableAgent(name="Examiner", llm_config=llm_config_examiner, system_message="You are an examiner and part of a trio that work on creating questions out of a given subject. your role is to always craft 2-3 test questions to evaluate understanding of recieved text.")

user_proxy = autogen.UserProxyAgent(
    name = "user_proxy",
    human_input_mode= "NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config=llm_config,
    code_execution_config=False,
   system_message = "Reply TERMINATE if the task has been solved for your full satisfaction. Or reply CONTINUE if the task is not solved yet",
)

topic=input("Enter a topic: ")

response=user_proxy.initiate_chat(
    researcher,
    message=f'Develop ideas for teaching someone new to the subject "{topic}"'
)
response=researcher.initiate_chat(
    writer,
    message=f'Use one these ideas to write a piece of text to explain {topic}.  Ideas:"{response}"'
)

response=writer.initiate_chat(
    examiner ,
    message=f'Crafts 2-3 test questions to evaluate understanding of this writing: {response}.'
)

print(response)