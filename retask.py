from secret import token
import telebot
import speech_recognition as sr

tasks = {}
done_tasks = {}

bot = telebot.TeleBot(token)

@bot.message_handler(commands= ['start'])
def start(message):
    print ("У меня начался рабочий день!")
    bot.send_message(message.chat.id, '<b>Я Вас слушаю)</b>', parse_mode='html')

@bot.message_handler(commands=['add'])
def add(msg):
    global tasks  # DONE: delete /add from task desctription
    if msg.chat.id not in tasks:
        tasks[msg.chat.id] = []
    if msg not in tasks[msg.chat.id]:  # DONE: tasks for different people should be separated
        tasks[msg.chat.id]
        tasks[msg.chat.id].append(msg.text[4:].strip())
    for tid in sorted(list(tasks.keys())):
        print(tasks[tid])
 
def format_task(task, i=0):
    return ('%3i. %s \n' % (i, task))
        
def format_list(task_list):
    reply = ''
    i = 1
        #print('preparing ' + task)
    for tsk in task_list:
            reply += format_task(tsk, i)
            i += 1
    return reply

@bot.message_handler(commands=['list'])
def tlist(msg):  # add "done" for done tasks with time
    global tasks
    print(type(tasks))
    print(tasks)
    if msg.chat.id not in tasks:
        tasks[msg.chat.id] = []
    reply = format_list(tasks[msg.chat.id])
    print(reply)
    print (len(tasks[msg.chat.id]))
    if len(tasks[msg.chat.id]) == 0:
        bot.send_message(msg.chat.id, '<b>У Вас нет задач, добавьте их, или отдохните!</b>', parse_mode='html')
    bot.send_message(
        msg.chat.id,
        reply,
        parse_mode='html'
    )
   
    
@bot.message_handler(commands=['done'])
def done(msg):
    global done_tasks
    if msg.chat.id not in done_tasks:
        done_tasks[msg.chat.id] = []
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
                reply += '<b>%i task does not exists</b>\n' % (task_id)
            else:
                done_tasks[msg.chat.id].append(tasks[msg.chat.id][task_id-1])
                tasks[msg.chat.id][task_id-1] = '<s>%s</s>' % tasks[msg.chat.id][task_id-1]
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
    if msg.chat.id not in tasks:
        tasks[msg.chat.id] = []
    tasks = {}
    bot.send_message(msg.chat.id, '<b>Очистила!</b>', parse_mode='html')
    
    
bot.polling(none_stop=True) 