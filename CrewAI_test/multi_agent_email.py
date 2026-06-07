import os
from crewai import Agent, Task, Crew, Process, LLM
from tool.custom_tools import *
from dotenv import load_dotenv, find_dotenv
# from langchain_community.chat_models import ChatOpenAI
# # #线上大模型--API方式
# _ = load_dotenv(find_dotenv())
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# base_url = os.environ['OPENAI_BASE_URL']
# client = ChatOpenAI(model_name="gpt-3.5-turbo")
# 本地大模型--ollama方式
# TODO 0.提前定义好LLM大语言模型
qw = LLM(
    model="ollama/qwen3:8b",
    base_url='http://localhost:11434'
)
# TODO 1.创建智能体
# 1.1 创建作家智能体
writer = Agent(
    role="作家",
    goal="根据用户的需求,创作出情感比较丰富的文字(要求字数在300左右)",
    backstory="你作为一个非常优秀的作家,拥有丰富的写作经验,最擅长编写情感丰富的文章",
    verbose=True,
    allow_delegation=False,
    llm=qw
)
# 1.2 创建编辑者智能体
editor = Agent(
    role="编辑者",
    goal="请你对上面作家创作的文章进行编辑优化,让内容更加丰富,编辑成标准的书信格式",
    backstory="""你作为一个非常专业的编辑,你在编辑书信方面有很多年的经验,你需要将文章编写成书信格式,
            并将编辑好的书信内容存储到本地磁盘上,你必须使用tools列表中的store_poesy_to_txt工具
            将编辑好的书信内容存储到指定文件中
    """,
    tools=[store_poesy_to_txt],
    verbose=True,
    allow_delegation=False,
    llm=qw
)
# 1.3 创建编辑者智能体
sender = Agent(
    role="寄信者",
    goal="请你把上面编辑者编辑并优化好的书信以邮件的形式发送给用户指定的收件人,必须保证发送成功,再结束!!!",
    backstory="""你作为一个非常专业的寄信者,在发邮件方面有多年的经验,请你把上面编辑者
        优化好的情书发送给指定收件人,你必须使用tools中的send_email工具将书信发送到指定邮箱
    """,
    tools=[send_email],
    verbose=True,
    allow_delegation=False,
    llm=qw
)
# TODO 2.构建任务,指定智能体
# todo 先获取用户的需求
user_input = input("请您输入您写情书的要求和收件人:")
# 2.1 写情书
task1 = Task(
    description=f"根据用户的需求:{user_input},生成一个非常浪漫真挚的情书",
    expected_output="已经生成一份情感真挚的情书(300字左右)",
    agent=writer
)
# 2.2 编辑情书为书信格式
task2 = Task(
    description=f"对上述写好的情书进行编辑优化,使其更加丰富,符合书信格式",
    expected_output="已经编辑并优化好情书为书信格式,并且成功保存到本地磁盘上",

    agent=editor
)
# 2.3 编辑情书为书信格式
task3 = Task(
    description=f"把优化为书信格式的情书,进行邮件发送到指定邮箱,这个很重要!必须要发送成功",
    expected_output="发送邮件任务已经调用成功,请查看邮箱",

    agent=sender
)
# TODO 3.创建Crew对象,传入智能体和任务并触发运行
crew = Crew(
    agents=[writer, editor, sender],
    tasks=[task1, task2, task3],
    verbose=True,
    Process=Process.sequential  # 当前是顺序执行,后续如果需要并行执行,请修改为Process.parallel
)
print('------------------------------------------')
# todo 触发执行
result = crew.kickoff()
print(result)