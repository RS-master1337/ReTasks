from secret import token
import telebot
import speech_recognition as sr
from datetime import datetime

class Tasks(dict):  # this class keeps, loads, saves, adds and clears tasks
    
    def __getitem__(self, key):
        if key not in self:
            self[key] = []
        return super(Tasks, self).__getitem__(key)
    # def __init__(self):  # calls when object is created
    
    def __add__(self, msg):
        print('koko')
    
    def __iadd__(self, msg):
        print('kuku')
        if msg.chat.id not in self.tasks:
            self.tasks[msg.chat.id] = []
  
tasks = Tasks()  # like classic dict but better

bot = telebot.TeleBot(token)

@bot.message_handler(commands= ['start'])
def start(message):
    print ("У меня начался рабочий день!")
    bot.send_message(message.chat.id, '<b>Я Вас слушаю)</b>', parse_mode='html')

@bot.message_handler(commands=['add'])
def add(msg):
    global tasks  # DONE: delete /add from task desctription
    if msg not in tasks[msg.chat.id]:  # DONE: tasks for different people should be separated
        msg.text = msg.text[4:].strip()
        msg.progresstime = []
        msg.autotime = True
        msg.done = None
        tasks[msg.chat.id].append(msg)#.text[4:].strip())
    for tid in sorted(list(tasks.keys())):
        print(tasks[tid])
 
def format_task(task, i=0):
    if task.done is None:
        return '%3i. %s \n' % (i, task.text)
    return '%3i. <s>%s</s> \n' % (i, task.text)
        
def format_list(task_list):
    reply = ' '
    i = 1
        #print('preparing ' + task)
    for tsk in task_list:
        reply += format_task(tsk, i)
        i += 1
    return reply

@bot.message_handler(commands=['list'])
def tlist(msg):  # add "done" for done tasks with time
    #global tasks
    reply = format_list(tasks[msg.chat.id])
    print(reply)
    print (len(tasks[msg.chat.id]))
    if len(tasks[msg.chat.id]) == 0:
        bot.send_message(
            msg.chat.id,
            '<b>У Вас нет задач, добавьте их или отдохните!</b>',
            parse_mode='html')
    bot.send_message(
        msg.chat.id,
        reply,
        parse_mode='html'
    )
   
    
@bot.message_handler(commands=['done'])
def done(msg):
    if msg.text.strip() == '/done':
        reply = format_list(done_tasks[msg.chat.id])
        print (reply)
        bot.send_message(
            msg.chat.id,
            reply,
            parse_mode='html'
        ) 
        return
    reply = ''
    new_done_list = msg.text.split()
    for elem in new_done_list:
        if elem.isdigit():
            task_id = int(elem)
            if task_id > len(tasks[msg.chat.id]):
                reply += '<b>%i - такой задачи нет</b>\n' % (task_id)
            else:
                tasks[msg.chat.id][task_id-1].done = int(datetime.now().timestamp())
    reply += format_list(tasks[msg.chat.id])
    bot.send_message(
        msg.chat.id,
        reply,
        parse_mode='html'
    ) 
#   for(b= 1; b <= i; b++)
#  def parse_done_list(user_input):
 #   numbers = []
 #   tasks = []
#    task = ''
# add done с номером, чтобы пометить таску, как сделанную

@bot.message_handler(commands=['clear'])
def clear(msg):
    global done_tasks
    if msg.chat.id not in done_tasks:
        done_tasks[msg.chat.id] = []
    done_tasks[msg.chat.id] = []
    global tasks
    tasks = Tasks()
    bot.send_message(msg.chat.id, '<b>Очистила!</b>', parse_mode='html')
    
    
bot.polling(none_stop=True)