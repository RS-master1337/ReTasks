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
        if msg not in self[msg.chat.id]:  # DONE: tasks for different people should be separated
            msg.text = msg.text[4:].strip()
            msg.progresstime = []
            msg.autotime = True
            msg.done = None
            self[msg.chat.id].append(msg)
        return self
  
tasks = Tasks()  # like classic dict but better

bot = telebot.TeleBot(token)

@bot.message_handler(commands= ['start'])
def start(message):
    print ("У меня начался рабочий день!")
    bot.send_message(message.chat.id, '<b>Я Вас слушаю)</b>', parse_mode='html')

@bot.message_handler(commands=['add'])
def add(msg):
    global tasks  # DONE: delete /add from task desctription
    tasks += msg
    for tid in sorted(list(tasks.keys())):
        for task in tasks[tid]:
            print('\t' + task.text)
 
def format_task(task, i=0):
    if task.done is None:
        return '%3i. %s \n' % (i, task.text)
    return '%3i. \u2705 <s>%s</s> at %s\n' % (
        i,
        task.text,
        datetime.fromtimestamp(task.done).strftime('%Y-%m-%d %H:%M'))
        
def format_list(task_list, filtr='all'):
    reply = ''
    i = 1
        #print('preparing ' + task)
    for tsk in task_list:
        if (filtr == 'done' and tsk.done is not None) or (
            filtr == 'not_done' and tsk.done is None) or (
            filtr not in ['done', 'not_done']):
            reply += format_task(tsk, i)
        i += 1
    if reply == '':
        reply = '<b>У Вас нет задач, добавьте их или отдохните!</b>'
    return reply

@bot.message_handler(commands=['list'])
def tlist(msg):  # add "done" for done tasks with time
    #global tasks
    if msg.text[5:].strip() == 'not done':
        reply = format_list(tasks[msg.chat.id], 'not_done')
        print (reply)
        bot.send_message(
            msg.chat.id,
            reply,
            parse_mode='html'
        )
        return
    reply = format_list(tasks[msg.chat.id])
    bot.send_message(
        msg.chat.id,
        reply,
        parse_mode='html'
    )
   
    
@bot.message_handler(commands=['done'])
def done(msg):
    if msg.text.strip() == '/done':
        reply = format_list(tasks[msg.chat.id], 'done')
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