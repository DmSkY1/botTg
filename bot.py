import asyncio
import tracemalloc
from Function import *
from aiogram.utils.markdown import hlink
import googletrans
from aiogram import Bot, Dispatcher, types, executor
import urllib.parse
from googletrans import Translator
import requests
from ParserNhentai import *
import time
import os
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from math import *
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputMedia, InputMediaPhoto, InputMediaAnimation
import json
import os.path
from datetime import datetime


Token = "Token"
bot = Bot(token=Token)
dp = Dispatcher(bot)
translator = Translator()
parser = Parser()


def stat():
    with open('Json/statistics.json', "r") as f:
        templates = json.loads(f.read())



    stat_bot_work = f"""
<b>📊Статистика бота:📊</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<b><u>Список используемых комманд:</u></b>
<i>translate</i> - {templates["translate"]}
<i>animeframesearchbyphoto</i> - {templates["animeframesearchbyphoto"]}
<i>animeframesearchbyurl</i> - {templates["animeframesearchbyurl"]}
<i>start/help</i> - {templates["start"]}
<i>nhentaicheck</i> - {templates["nhentaicheck"]}
<i>eropic</i> - {templates["eropic"]}
<i>ecchipic</i> - {templates["ecchipic"]}
<i>paizuripic</i> - {templates["paizuripic"]}
<i>asspic</i> - {templates["asspic"]}
<i>oralipic</i> - {templates["oralipic"]}
<i>milfpic</i> - {templates["milfpic"]}
<i>maidpic</i> - {templates["maidpic"]}
<i>waifupic</i> - {templates["waifupic"]}
<i>marinkitagawapic</i> - {templates["marinkitagawapic"]}
<i>moricalliopepic</i> - {templates["moricalliopepic"]}
<i>raidenshogunpic</i> - {templates["raidenshogunpic"]}
<i>oppaipic</i> - {templates["oppaipic"]}
<i>uniformpic</i> - {templates["uniformpic"]}
<i>hentaipic</i> - {templates["hentaipic"]}
<i>nekopic</i> - {templates["nekopic"]}
<i>trappic</i> - {templates["trappic"]}
<i>blowjobpic </i>- {templates["blowjobpic"]}
<i>cringegif</i> - {templates["cringegif"]}
<i>smilegif</i> - {templates["smilegif"]}
<i>nomgif</i> - {templates["nomgif"]}
<i>kickgif</i> - {templates["kickgif"]}
<i>blushgif</i> - {templates["blushgif"]} 
<i>yeetgif</i> - {templates["yeetgif"]}
<i>cuddlegif</i> - {templates["cuddlegif"]}
<i>crygif</i> - {templates['crygif']}
<i>myprofile</i> - {templates["myprofile"]}
<i>rewrite</i> - {templates["rewrite"]} 
<i>statistics</i> - {templates["statistics"]}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
🕒Дата последнего обновления: <b><i>{datetime.now().date()}</i></b>    <i>{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}</i>
"""
    f.close()
    return stat_bot_work



admin_menu = f"""
Команды для администраторов:
/helpadmin - команд для админа.
/mute - 
/setstat -
/getadmin -
/setadmin -
/userlist -
/getuser -
/senduser -
"""


a = list()
"""FUNCTION"""

def write_json(key):
    with open('Json/statistics.json', "r+") as f:
        data = json.load(f)
        data[key] += 1
    with open('Json/statistics.json', 'w') as f:
        f.write(json.dumps(data, indent=4))

def User_Exist(user_id):
    a = True
    with open('Json/UserList.json', "r") as f:
        data = json.load(f)
    for i in data["Users"]:
        if f'{user_id}' in i:
            a = False
    return a
def totality_command(user_id, command):
    times = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year} ------ {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
    Last_Activity(user_id, times)
    Last_Command(user_id, command)


def get_name(user_id):
    with open("Json/UserList.json", "r") as f:
        data = json.load(f)
    for i in data["Users"]:
        try:
            return i[user_id]['User_name']
        except:pass

def get_admin(user_id):
    with open('Json/UserList.json', "r+") as f:
        data = json.load(f)
    for i in data["Users"]:
        try: i[user_id]["Admin"] =True
        except: pass
    with open('Json/UserList.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def set_admin(user_id):
    with open('Json/UserList.json', "r+") as f:
        data = json.load(f)
    for i in data["Users"]:
        try: i[user_id]["Admin"] =False
        except: pass
    with open('Json/UserList.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def new_user(user_id, name, usr_photo, data, data_t):
    conf = {
        f'{user_id}':{
            "MainAdmin": False,
            "Admin": False,
            'User_name': name,
            "User_photo": usr_photo,
            "Date_reg": data,
            "Date_time": data_t,
            "Last_Activity": None,
            "Last_Command": None
        }
    }
    with open('Json/UserList.json', "r") as f:
        data = json.load(f)
    if User_Exist(user_id):

        data["Users"].append(conf)
        with open('Json/UserList.json', 'w') as f:
            json.dump(data, f, indent=4)

#json.dump(data, ensure_ascii=False, indent=4)
def infadmin(user_id):
    with open('Json/UserList.json', "r") as f:
        data = json.loads(f.read())
    for i in data["Users"]:
        try:
            if i[f'{user_id}']["Admin"]:return True
            else:return False
        except:pass

def infsenadmin(user_id):
    with open('Json/UserList.json', "r") as f:
        data = json.loads(f.read())
    for i in data["Users"]:
        try:
            if i[f'{user_id}']["MainAdmin"]:return True
            else:return False
        except:pass

def setstat():
    with open('Json/statistics.json', "r+") as f:
        data = json.load(f)
    with open('Json/statistics.json', 'w') as f:
        for i in data:
            data[i] = 0
        f.write(json.dumps(data, indent=4))

def GetUrl(x):
    r = requests.get(f"https://api.waifu.im/search/?included_tags={x}").text
    item = json.loads(r)
    url = item["images"][0]["url"]
    return url
def GetUrlNeko():
    resp = requests.get("https://nekos.best/api/v2/neko")
    data = resp.json()
    return data["results"][0]["url"]
def GetUrlblowjobandtrap(x):
    resp = requests.get(f"https://api.waifu.pics/nsfw/{x}")
    data = resp.json()
    return data["url"]
def GetUrlGif(x):
    resp = requests.get(f"https://api.waifu.pics/sfw/{x}")
    data = resp.json()
    return data["url"]
def GetImage(name):
    lis = []
    try:
        lis.append(GetUrl(name))
    except Exception:
        lis.append(GetUrl(name))
        try:
            lis.append(GetUrl(name))
        except Exception:
            lis.append(GetUrl(name))
    return lis[0]

def sran(user_id):
    js = requests.post("https://api.trace.moe/search",
                       data=open(f"{user_id}.jpg", "rb"),
                       headers={"Content-Type": "image/jpeg"}
                       ).json()
    result = f'''
                        <strong>✅Результат✅</strong>
                <strong>📄Название:</strong> {js["result"][0]["filename"]}
                <strong>🗂Эпизод:</strong> {js["result"][0]['episode']}
                <strong>⏳Время:</strong> {time.strftime("%H:%M:%S", time.gmtime(js["result"][0]["from"]))} - {time.strftime("%H:%M:%S", time.gmtime(js["result"][0]["to"]))}
                <strong>📈Слвпадение:</strong> {float(js["result"][0]["similarity"]) * 100}%
                            '''
    return result

@dp.message_handler(commands = ["start", "help"])
async def Welcome(message: types.Message):
    totality_command(message.from_user.id, "/start")
    data = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"
    date_time = f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
    try:
        a = await message.from_user.get_profile_photos()
        id = a.photos[0][1].file_id
    except: pass
    new_user(message.from_user.id, message.from_user.username, id, data, date_time)
    write_json("start")
    await message.reply("Привет, я наконец то заработал")

#@dp.message_handler()
#async def echo(message: types.Message):
#await bot.send_photo(message.chat.id, photo=url)
#https://www.nekos.fun/apidoc.html 100%
#https://waifu.pics/docs
#https://soruly.github.io/trace.moe-api/#/docs

"""BUTTON"""

keyboard = InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("🇺🇸English", callback_data="enb"),
        types.InlineKeyboardButton("🇷🇺Русский", callback_data="rub"),
        types.InlineKeyboardButton("فارسی🇦🇪", callback_data="arb"),
        types.InlineKeyboardButton("🇮🇹Italiano", callback_data="itb"),
        types.InlineKeyboardButton("🇫🇷Français", callback_data="frb"),
        types.InlineKeyboardButton("🇩🇪Deutsch", callback_data="geb"),
        types.InlineKeyboardButton("🇵🇹Português", callback_data="pob"),
        types.InlineKeyboardButton("🇹🇷Türkçe", callback_data="tub"),
        types.InlineKeyboardButton("🇸🇰Slovenský", callback_data="slb"),
        types.InlineKeyboardButton("עברית🇮🇱", callback_data="ivb"),
        types.InlineKeyboardButton("🇪🇸Español", callback_data="esb"),
        types.InlineKeyboardButton("🇯🇵日本", callback_data="jab"),
        types.InlineKeyboardButton("🇵🇱Polski", callback_data="plb"),
        types.InlineKeyboardButton("🇰🇷한국인", callback_data="kob"),
        types.InlineKeyboardButton("🇰🇿қазақ", callback_data="kzb"),
        types.InlineKeyboardButton("🇨🇳中国人", callback_data="chb")
    )
keyboard2 = InlineKeyboardMarkup().add(
    InlineKeyboardButton("ДА!", callback_data="yes"),
    InlineKeyboardButton("НЕТ!", callback_data="no")
)
erobtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="erob"))
henbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="henb"))
eccbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="eccb"))
paibtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="paib"))
assbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="assb"))
orabtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="orab"))
milbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="milb"))
maibtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="maib"))
waibtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="waib"))
marinbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="marinb"))
raidenbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="raidenb"))
moribtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="morib"))
oppbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="oppb"))
unibtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="unib"))
nekobtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="nekob"))
trapbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="trapb"))
blowbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="blowb"))
cringetn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="cringeb"))
smilebtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="smileb"))
nombtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="nomb"))
kickbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="kickb"))
blushbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="blushb"))
yeetbtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="yeetb"))
cuddlebtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="cuddleb"))
crybtn = InlineKeyboardMarkup().add(types.InlineKeyboardButton("Следующая➡", callback_data="cryb"))

"""CALLBACK_QUERY"""

@dp.callback_query_handler(lambda call: call.data == "yes")
async def edit_msg1(q: types.CallbackQuery):
    setstat()
    des = "<i><b>✅Данные успешно удалены!✅</b></i>"
    await q.message.edit_text(des, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "no")
async def edit_msg1(q: types.CallbackQuery):
    des = "<i><b>✅Комманда успешно отменена!✅</b></i>"
    await q.message.edit_text(des, parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data == "enb")
async def edit_msg1(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='en').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "rub")
async def edit_msg2(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='ru').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "arb")
async def edit_msg3(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='ar').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "itb")
async def edit_msg1(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='it').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "frb")
async def edit_msg2(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='fr').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "geb")
async def edit_msg3(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='de').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "pob")
async def edit_msg1(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='pt').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "tub")
async def edit_msg2(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='tr').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "slb")
async def edit_msg3(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='sl').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "ivb")
async def edit_msg1(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='iv').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "esb")
async def edit_msg2(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='es').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "jab")
async def edit_msg3(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='ja').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "plb")
async def edit_msg1(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='pl').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "kob")
async def edit_msg2(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='ko').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "kzb")
async def edit_msg3(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='kk').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "chb")
async def edit_msg3(q: types.CallbackQuery):
    m1 = q.message.text.replace('/translate ', '')
    await q.message.edit_text(f"<i>{translator.translate(m1, dest='zh-tw').text}</i>", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda call: call.data == "erob")
async def edit_msg3(q: types.CallbackQuery):
    try:photo = GetUrl("ero")
    except Exception:photo = GetUrl("ero")
    photo = GetUrl("ero")
    file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode = "HTML")
    await q.message.edit_media(file, reply_markup=erobtn)
@dp.callback_query_handler(lambda call: call.data == "henb")
async def edit_msg3(q: types.CallbackQuery):
    try:photo = GetUrl("hentai")
    except Exception:photo = GetUrl("hentai")
    photo = GetUrl("hentai")
    file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode = "HTML")
    await q.message.edit_media(file, reply_markup=henbtn)
@dp.callback_query_handler(lambda call: call.data == "eccb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("ecchi")
        photo = GetUrl("ecchi")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=eccbtn)
    except Exception:
        photo = GetUrl("ecchi")
        photo = GetUrl("ecchi")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode = "HTML")
        await q.message.edit_media(file, reply_markup=eccbtn)
@dp.callback_query_handler(lambda call: call.data == "assb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("ass")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=assbtn)
    except Exception:
        photo = GetUrl("ass")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=assbtn)
        try:
            photo = GetUrl("ass")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=assbtn)
        except Exception:
            photo = GetUrl("ass")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=assbtn)

@dp.callback_query_handler(lambda call: call.data == "paib")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("paizuri")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=paibtn)
    except Exception:
        try:
            photo = GetUrl("paizuri")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=paibtn)
        except Exception:
            photo = GetUrl("paizuri")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=paibtn)



@dp.callback_query_handler(lambda call: call.data == "orab")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("oral")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=orabtn)
    except Exception:
        photo = GetUrl("oral")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=orabtn)
        try:
            photo = GetUrl("oral")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=orabtn)
        except Exception:
            photo = GetUrl("oral")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=orabtn)
@dp.callback_query_handler(lambda call: call.data == "milb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("milf")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=milbtn)
    except Exception:
        try:
            photo = GetUrl("milf")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=milbtn)
        except Exception:
            photo = GetUrl("milf")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=milbtn)

@dp.callback_query_handler(lambda call: call.data == "maib")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("maid")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=maibtn)
    except Exception:
        photo = GetUrl("maid")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=maibtn)
        try:
            photo = GetUrl("maid")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=maibtn)
        except Exception:
            photo = GetUrl("maid")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=maibtn)
@dp.callback_query_handler(lambda call: call.data == "waib")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("waifu")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=waibtn)
    except Exception:

        try:
            photo = GetUrl("waifu")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=waibtn)
        except Exception:
            photo = GetUrl("waifu")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=waibtn)

@dp.callback_query_handler(lambda call: call.data == "marinb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("marin-kitagawa")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=marinbtn)
    except Exception:
        try:
            photo = GetUrl("marin-kitagawa")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=marinbtn)
        except Exception:
            photo = GetUrl("marin-kitagawa")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=marinbtn)

@dp.callback_query_handler(lambda call: call.data == "raidenb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("raiden-shogun")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=raidenbtn)
    except Exception:
        try:
            photo = GetUrl("raiden-shogun")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=raidenbtn)
        except Exception:
            photo = GetUrl("raiden-shogun")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=raidenbtn)

@dp.callback_query_handler(lambda call: call.data == "morib")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("mori-calliope")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=moribtn)
    except Exception:
        try:
            photo = GetUrl("mori-calliope")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=moribtn)
        except Exception:
            photo = GetUrl("mori-calliope")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=moribtn)

@dp.callback_query_handler(lambda call: call.data == "oppb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("oppai")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=oppbtn)
    except Exception:
        try:
            photo = GetUrl("oppai")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=oppbtn)
        except Exception:
            photo = GetUrl("oppai")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=oppbtn)

@dp.callback_query_handler(lambda call: call.data == "unib")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrl("uniform")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=unibtn)
    except Exception:
        try:
            photo = GetUrl("uniform")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=unibtn)
        except Exception:
            photo = GetUrl("uniform")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode = "HTML")
            await q.message.edit_media(file, reply_markup=unibtn)
@dp.callback_query_handler(lambda call: call.data == "nekob")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrlNeko()
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=nekobtn)
    except Exception:
        try:
            photo = GetUrlNeko()
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=nekobtn)
        except Exception:
            photo = GetUrlNeko()
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=nekobtn)

@dp.callback_query_handler(lambda call: call.data == "trapb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrlblowjobandtrap("trap")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=trapbtn)
    except Exception:
        try:
            photo = GetUrlblowjobandtrap("trap")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=trapbtn)
        except Exception:
            photo = GetUrlblowjobandtrap("trap")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=trapbtn)

@dp.callback_query_handler(lambda call: call.data == "blowb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        photo = GetUrlblowjobandtrap("blowjob")
        file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=blowbtn)
    except Exception:
        try:
            photo = GetUrlblowjobandtrap("blowjob")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=blowbtn)
        except Exception:
            photo = GetUrlblowjobandtrap("blowjob")
            file = InputMedia(media=photo, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                              parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=blowbtn)
#######
@dp.callback_query_handler(lambda call: call.data == "cringeb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("cringe")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=cringetn)
    except Exception:
        try:
            gif = GetUrlGif("cringe")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=cringetn)
        except Exception:
            gif = GetUrlGif("cringe")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=cringetn)
@dp.callback_query_handler(lambda call: call.data == "cryb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("cry")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=crybtn)
    except Exception:
        try:
            gif = GetUrlGif("cry")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=crybtn)
        except Exception:
            gif = GetUrlGif("cry")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=crybtn)
@dp.callback_query_handler(lambda call: call.data == "smileb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("smile")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=smilebtn)
    except Exception:
        try:
            gif = GetUrlGif("smile")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=smilebtn)
        except Exception:
            gif = GetUrlGif("smile")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=smilebtn)
@dp.callback_query_handler(lambda call: call.data == "cuddleb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("cuddle")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=cuddlebtn)
    except Exception:
        try:
            gif = GetUrlGif("cuddle")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=cuddlebtn)
        except Exception:
            gif = GetUrlGif("cuddle")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=cuddlebtn)
@dp.callback_query_handler(lambda call: call.data == "kickb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("kick")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=kickbtn)
    except Exception:
        try:
            gif = GetUrlGif("kick")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=kickbtn)
        except Exception:
            gif = GetUrlGif("kick")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=kickbtn)
@dp.callback_query_handler(lambda call: call.data == "nomb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("nom")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=nombtn)
    except Exception:
        try:
            gif = GetUrlGif("nom")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=nombtn)
        except Exception:
            gif = GetUrlGif("nom")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=nombtn)
@dp.callback_query_handler(lambda call: call.data == "blusheb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("blush")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=blushbtn)
    except Exception:
        try:
            gif = GetUrlGif("blush")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=blushbtn)
        except Exception:
            gif = GetUrlGif("blush")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=blushbtn)
@dp.callback_query_handler(lambda call: call.data == "yeetb")
async def edit_msg3(q: types.CallbackQuery):
    try:
        gif = GetUrlGif("yeet")
        file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                          parse_mode="HTML")
        await q.message.edit_media(file, reply_markup=yeetbtn)
    except Exception:
        try:
            gif = GetUrlGif("yeet")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=yeetbtn)
        except Exception:
            gif = GetUrlGif("yeet")
            file = InputMediaAnimation(media=gif, caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>',
                                       parse_mode="HTML")
            await q.message.edit_media(file, reply_markup=yeetbtn)

"""COMMAND"""

#https://ru.stackoverflow.com/questions/1327154/%D0%9A%D0%B0%D0%BA-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D0%BE-%D1%82%D0%B0%D0%B9%D0%BC%D0%B5%D1%80%D1%83-aiogram

#https://api.telegram.org/bot5833407622:AAGbJ5lxLO2u7yGzNgb4M5n6SPxsyxG6oM0/sendPhoto?chat_id=1021576974&photo=https://cdn.dogehls.xyz/galleries/2217312/1.jpg

@dp.message_handler(commands="nhentaicheck", content_types= types.ContentType.ANY)
async def nhentai(message: types.Message):
    totality_command(message.from_user.id, "/nhentaicheck")
    await message.answer("⚠Если бот не отвечат на ваш код более чем 10 сек, то код введен неправильно или  такой манги несуществует.⚠\n\nВведите уникальный код для поиска манги. Например: #122312")
    async def check(message: types.Message):#проверка на ошибку кода 200 404 доступа проверка через реквест
        noerror = 0
        start3 = time.time()
        if message.text.startswith("#"):
            if message.text.replace("#", "").isdigit() and len(message.text)==7 and requests.get(f"https://nhentai.cam/g/{message.text.replace('#', '')}"):
                write_json("nhentaicheck")
                await message.reply("<strong>Манга найдена!</strong> Производится отправка. ⚠ВНИМАНИЕ: ПРОЦЕСС ОТПРАВКИ ЗАПУЩЕН И НЕ МОЖЕТ БЫТЬ ОТМЕНЕН⚠", parse_mode='HTML')
                noerror = 0
                logo = parser.GetLogo(message.text.replace("#", ""))
                name = parser.GetName(message.text.replace("#", ""))
                page = parser.GetPage(int(message.text.replace("#", "")))
                result =f"""
<strong>Результат:</strong>
<strong>🇺🇸Название №1:</strong> <i>{name[0]}</i>  
<strong>🇯🇵Название №2:</strong> <i>{name[1]}</i>
🔐Уникальный код: <i><a href="{f'https://nhentai.cam/g/{message.text.replace("#", "")}'}">#{message.text.replace("#", "")}</a></i>
🗒Количество страниц: <i>{page}</i>
🕒Примерное время поиска манги: <i>{page*0.5} сек.</i>"""
                await bot.send_photo(message.chat.id, photo=logo, caption=result, parse_mode="HTML")
                start1 = time.time()
                mess = parser.ParserImage(page, int(message.text.replace("#", ""))).replace('1.', '&')
                end1 = time.time() - start1
                start2 = time.time()
                for i in range(1, page+1):
                    r = requests.get(f"https://api.telegram.org/bot{Token}/sendPhoto?chat_id={message.chat.id}&photo={mess.replace('&', f'{i}.')}")
                    if r.status_code == 200:
                        noerror +=1
                end2 = time.time() - start2
            else:
                await message.answer("❌Unique_Code_Error❌: Проверьте правильность написания кода. В коде не может содеожаться посторонних символов кроме 6 цифр. Либо такой страницы не существует!!")
            end3 = time.time() - start3
            report = f"""
<strong>📊Отчет об отправке</strong>
📬Страниц доставлено: <strong><i>{noerror} из {page}</i></strong>
🔍Время обработки манги: <strong><i>{ceil(end1)} сек.</i></strong>
📩Время отправки манги: <strong><i>{ceil(end2)} сек.</i></strong>
⚙Время обработки комманды: <strong><i>{ceil(end3)} сек.</i></strong>
        """
            await message.answer(report, parse_mode="HTML")
        else:
            pass
    dp.register_message_handler(check)

@dp.message_handler(commands= "translate") # доделать вынести в функцию
async def echo(message: types.Message):
    totality_command(message.from_user.id, "/translate")
    st = """
    ⚠Если переводчик переводит не правильно, то убедитесь в правельности написаня своего текста. Скорость перевода может быть разной 1-2 сек или 5 сек и более⚠️
    """
    await message.answer(st)
    await message.answer(message.text.replace('/translate ', ''), reply_markup=keyboard)
    write_json("translate")

@dp.message_handler(commands="eropic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/eropic")
    write_json("eropic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage("ero"), caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=erobtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage("ero"), caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=erobtn)

@dp.message_handler(commands="ecchipic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/ecchipic")
    write_json("ecchipic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage("ecchi"),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=eccbtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage("ecchi"),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=eccbtn)

@dp.message_handler(commands="paizuripic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/paizuripic")
    write_json("paizuripic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage("paizuri"),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=paibtn)
    except:
        await bot.send_photo(message.chat.id, photo=GetImage("paizuri"),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=paibtn)

@dp.message_handler(commands="asspic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/asspic")
    write_json("asspic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage("ass"),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=assbtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage("ass"),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=assbtn)

@dp.message_handler(commands="oralipic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/oralipic")
    write_json("oralipic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('oral'), caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=orabtn)

    except Exception:

        await bot.send_photo(message.chat.id, photo=GetImage('oral'), caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=orabtn)

@dp.message_handler(commands="milfpic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/milfpic")
    write_json("milfpic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('milf'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=milbtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('milf'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=milbtn)

@dp.message_handler(commands="maidpic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/maidpic")
    write_json("maidpic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('maid'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=maibtn)
    except:
        await bot.send_photo(message.chat.id, photo=GetImage('maid'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=maibtn)

@dp.message_handler(commands="waifupic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/waifupic")
    write_json("waifupic")
    try:await bot.send_photo(message.chat.id, photo=GetImage('waifu'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=waibtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('waifu'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=waibtn)

@dp.message_handler(commands="marinkitagawapic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/marinkkitagawapic")
    write_json("marinkitagawapic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('marin-kitagawa'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=marinbtn)
    except Exception:

        await bot.send_photo(message.chat.id, photo=GetImage('marin-kitagawa'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=marinbtn)

@dp.message_handler(commands="moricalliopepic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/moricalliopepic")
    write_json("moricalliopepic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('mori-calliope'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=moribtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('mori-calliope'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=moribtn)

@dp.message_handler(commands="raidenshogunpic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/raidenshogunpic")
    write_json("raidenshogunpic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('raiden-shogun'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=raidenbtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('raiden-shogun'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=raidenbtn)

@dp.message_handler(commands="oppaipic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/oppaipic")
    write_json("oppaipic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('oppai'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=oppbtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('oppai'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=oppbtn)


@dp.message_handler(commands="uniformpic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/uniformpic")
    write_json("uniformpic")
    try:await bot.send_photo(message.chat.id, photo=GetImage('uniform'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=unibtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('uniform'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=unibtn)

@dp.message_handler(commands="hentaipic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/hentaipic")
    write_json("hentaipic")
    try:
        await bot.send_photo(message.chat.id, photo=GetImage('hentai'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=henbtn)
    except Exception:
        await bot.send_photo(message.chat.id, photo=GetImage('hentai'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML", reply_markup=henbtn)

@dp.message_handler(commands="nekopic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/nekopic")
    write_json("nekopic")
    try:
        await bot.send_photo(message.chat.id, photo=GetUrlNeko(),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                         reply_markup=nekobtn)

    except Exception:
        await bot.send_photo(message.chat.id, photo=GetUrlNeko('hentai'),
                     caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                     reply_markup=nekobtn)
@dp.message_handler(commands="trappic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/trappic")
    write_json("trappic")
    try:
        await bot.send_photo(message.chat.id, photo=GetUrlblowjobandtrap("trap"),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                         reply_markup=trapbtn)

    except Exception:
        await bot.send_photo(message.chat.id, photo=GetUrlblowjobandtrap("trap"),
                     caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                     reply_markup=trapbtn)
@dp.message_handler(commands="blowjobpic")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/blowjodpic")
    write_json("blowjobpic")
    try:
        await bot.send_photo(message.chat.id, photo=GetUrlblowjobandtrap('blowjob'),
                         caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                         reply_markup=blowbtn)

    except Exception:
        await bot.send_photo(message.chat.id, photo=GetUrlblowjobandtrap('blowjob'),
                     caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                     reply_markup=blowbtn)

@dp.message_handler(commands="cringegif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/cringegif")
    write_json("cringegif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('cringe'),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=cringetn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("cringe"),
                             caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                             reply_markup=cringetn)

@dp.message_handler(commands="smilegif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/smilegif")
    write_json("smilegif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('smile'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=smilebtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("smile"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=smilebtn)

@dp.message_handler(commands="nomgif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/nomgif")
    write_json("nomgif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('nom'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=nombtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("nom"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=nombtn)

@dp.message_handler(commands="kickgif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/kickgif")
    write_json("kickgif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('kick'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=kickbtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("kick"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=kickbtn)
@dp.message_handler(commands="blushgif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/blushgif")
    write_json("blushgif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('blush'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=blushbtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("blush"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=blushbtn)
@dp.message_handler(commands="yeetgif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/yeetgif")
    write_json("yeetgif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('yeet'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=yeetbtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("yeet"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=yeetbtn)
@dp.message_handler(commands="cuddlegif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/cuddlegif")
    write_json("cuddlegif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('cuddle'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=cuddlebtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("cuddle"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=cuddlebtn)
@dp.message_handler(commands="crygif")
async def getanimeneko(message: types.Message):
    totality_command(message.from_user.id, "/crygif")
    write_json("crygif")
    try:
        await bot.send_animation(message.chat.id, animation=GetUrlGif('cry'),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=crybtn)
    except:
        await bot.send_animation(message.chat.id, animation=GetUrlGif("cry"),
                                 caption='<a href="https://t.me/ZionLeysritt_bot">ZionLeysritt</a>', parse_mode="HTML",
                                 reply_markup=crybtn)
@dp.message_handler(commands="animeframesearchbyurl")
async def tracemooe(message: types.Message):
    totality_command(message.from_user.id, "/animeframesearchbyurl")
    write_json("animeframesearchbyurl")
    async def Search(message: types.Message):
        r = requests.get("https://api.trace.moe/search?url={}".format(urllib.parse.quote_plus(message.text)))
        js = r.json()
        result = f'''
        <strong>✅Результат✅</strong>
<strong>📄Название:</strong> {js["result"][0]["filename"]}
<strong>🗂Эпизод:</strong> {js["result"][0]['episode']}
<strong>⏳Время:</strong> {time.strftime("%H:%M:%S", time.gmtime(js["result"][0]["from"]))} - {time.strftime("%H:%M:%S", time.gmtime(js["result"][0]["to"]))}
<strong>📈Слвпадение:</strong> {float(js["result"][0]["similarity"]) * 100}%
        '''
        await message.answer(result, parse_mode='HTML')
        await bot.send_video(message.chat.id, js["result"][0]["video"])
    await message.answer("Введите URL для поиска")
    dp.register_message_handler(Search)

@dp.message_handler(commands="myprofile")
async def profile(m: types.Message):
    totality_command(m.from_user.id, "/myprofile")
    write_json("myprofile")
    mainadmin = ""
    admin = ""
    if infadmin(m.from_user.id):admin="Есть"
    else:admin="Нету"
    if infsenadmin(m.from_user.id):mainadmin="Есть"
    else:mainadmin="Нету"
    result = f"""
    Ваш профиль:
🙎‍♂Username: @{m.from_user.username}
🙎‍♂Имя: {m.from_user.first_name}
🌐ID: `{m.from_user.id}`
🛠Права старшего админа: {mainadmin}
🔧Права Админа: {admin}
    """
    try:
        a = await m.from_user.get_profile_photos()
        id = a.photos[0][1].file_id
    except:
        pass
    with open('Json/UserList.json', "r+") as f:
        data = json.load(f)
    for i in data["Users"]:
            try:
                if i[f"{m.from_user.id}"]["User_photo"] == id:
                    pass
                else:
                    i[f"{m.from_user.id}"]["User_photo"] = id
                    with open('Json/UserList.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)
            except:
                pass

        #a = await m.from_user.get_profile_photos()
        #foto = a.photos[0][1].file_id
        #id = foto
    try:
        await bot.send_photo(m.from_user.id, id, result, parse_mode="MARKDOWN")
    except:
        await m.answer(result, parse_mode="HTML")


@dp.message_handler(commands="user")
async def profile(m: types.Message):
    mess = m.text.replace("/user ", "")
    if mess == "/user":
        await m.answer("Вы не ввели id пользователя")
    elif mess.isdigit():
        with open('Json/UserList.json', "r+") as f:
            data = json.load(f)
        dt = ''
        dr = ""
        la = ""
        lc = ''
        un = ""
        sa = ""
        ad = ""
        id_photo = ""

        for i in data['Users']:
            try:
                dr = i[mess]["Date_reg"]
                la = i[mess]["Last_Activity"]
                dt = i[mess]["Date_time"]
                lc = i[mess]["Last_Command"]
                un = i[mess]["User_name"]
                sa = i[mess]["MainAdmin"]
                ad = i[mess]["Admin"]
                id_photo = i[mess]["User_photo"]
            except:
                pass
        totality_command(m.from_user.id, "/user")
        result = f"""
            Ваш профиль:
🙎‍♂Имя: {un}
🌐ID: `{mess}`
🛠Права старшего админа: {sa}
🔧Права Админа: {ad}
Дата регистрации: {dr}, {dt}
Последняя активность: {la}
Последняя команда: {lc}
            """
        try:

            id = id_photo
        except:
            pass
        with open('Json/UserList.json', "r+") as f:
            data = json.load(f)
        for i in data["Users"]:
            try:
                if i[f"{m.from_user.id}"]["User_photo"] == id:
                    pass
                else:
                    i[f"{m.from_user.id}"]["User_photo"] = id
                    with open('Json/UserList.json', 'w') as outfile:
                        json.dump(data, outfile, indent=4)
            except:
                pass

        try:

            await bot.send_photo(m.from_user.id, id, result, parse_mode="MARKDOWN")
        except:
            await m.answer(result, parse_mode="HTML")
    else:
        await m.reply("Такого id несушествует")





ls = [True]
@dp.message_handler(commands=["rewrite", 'r'])
async def Rewriter(message: types.Message):
    totality_command(message.from_user.id, "/rewrite")
    write_json("rewrite")
    ls[0] = True
    await message.answer("Введите текст для сокращения")
    async def regmess(message: types.Message):
        if ls[0]:
            await message.reply("✅Хорошо, Ваш текст поставлен в обработку!✅")
            getR = {
                "instances": [
                     {
                            "text": message.text,
                            "temperature": 0.9,
                            "top_k": 50,
                            "top_p": 0.7,
                            "range_mode": "bertscore"
                    }
                ]
            }
            resp = requests.post("https://api.aicloud.sbercloud.ru/public/v2/rewriter/predict", headers={'accept': 'application/json'}, json=getR)
            res = json.loads(resp.text)
            if resp.status_code == 422:
                await message.reply(json.loads(resp.text)['detail'][0]["msg"])
            elif not res.get('comment'):
                await message.answer(f'Лучший:\n`{res["prediction_best"]["bertscore"]}`', parse_mode="MARKDOWN")
                i = len(res['predictions_all'])
                num = 0
                if i > 3:
                    i=2
                for predictions in res['predictions_all'][:2]:
                    num+=1
                    await message.answer(f'{num} Вариант:\n`{predictions}`', parse_mode="MARKDOWN")
                try:

                    getR['instances'][0]['text'] = f"{res['prediction_best']['bertscore']}"
                    r2 = requests.post("https://api.aicloud.sbercloud.ru/public/v2/rewriter/predict", headers={'accept': 'application/json'}, json=getR)
                    res2 = json.loads(r2.text)
                    await message.answer(f"""Гиперсжатие(по лучшему варианту):\n`{res2["prediction_best"]["bertscore"]}`""", parse_mode="MARKDOWN")
                except Exception:
                    pass

            else: await message.reply(f"❌<strong>Произошла ошибка:</strong> <i>{resp.json().get('comment')}</i>❌", parse_mode='HTML')
        else: pass
        ls[0] = False
#json.loads(resp.text)['predictions_all'][1]
    dp.register_message_handler(regmess)

@dp.message_handler(commands="helpadmin")
async def helpadmin(msg: types.Message):
    totality_command(msg.from_user.id, "/helpadmin")
    if infadmin(msg.from_user.id):
        await msg.answer('тут что то должно быть')
    else:
        await msg.reply("🔐<b><i>Извините, но у вас недостаточно прав для того чтобы использовать эту комманду!</i></b>🔐", parse_mode="HTML")

@dp.message_handler(commands="userlist")
async def list(message: types.Message):
   totality_command(message.from_user.id, "/userlist")
   if infadmin(message.from_user.id):
        msg = "📜Список пользователей:\n"
        for key in user_list():
            msg+=f"`{key}` - @{user_list()[key]}\n"
        await message.answer(msg, parse_mode="MARKDOWN")
   else:
       await message.reply("🔐<b><i>Извините, но у вас недостаточно прав для того чтобы использовать эту комманду!</i></b>🔐", parse_mode="HTML")

@dp.message_handler(commands="getadmin")
async def getadmin(msg: types.Message):
    totality_command(msg.from_user.id, "/getadmin")
    if infsenadmin(msg.from_user.id):
        usr = msg.text[10:]
        if not User_Exist(usr):
            if not infadmin(usr):
                get_admin(usr)
                await bot.send_message(chat_id=int(usr), text="Вы нахначены админом")
                await msg.reply(f"<b>✅Пользователь</b> - <i>@{get_name(usr)}</i> стал <i><u>анминистратором!</u></i>✅", parse_mode="HTML")
            else:
                await msg.answer("<b>❌У этого пользователья уже есть права администрации!❌</b>", parse_mode="HTML")
        else:
            await msg.answer(f"<b>❌Пользователь с id: <u>{usr}</u> не найден!❌</b>", parse_mode="HTML")
    else:
        await msg.reply("🔐<b><i>Извините, но у вас недостаточно прав для того чтобы использовать эту комманду!</i></b>🔐", parse_mode="HTML")

@dp.message_handler(commands="setadmin")
async def getadmin(msg: types.Message):
    totality_command(msg.from_user.id, "/setadmin")
    if infsenadmin(msg.from_user.id):
        usr = msg.text[10:]
        if not User_Exist(usr):
            if infadmin(usr):
                set_admin(usr)
                await bot.send_message(chat_id=int(usr), text="Вы теперь не админ")
                await msg.reply(f"<b>✅Пользователь</b> - <i>@{get_name(usr)}</i> <i><u>разжалован!</u></i> до обычного <i>пользователя</i>✅", parse_mode="HTML")
            else:
                await msg.answer("<b>❌Вы не <b>можете</b> лишить этого пользователя прав <i>администрации</i>, т.к у него их <i><b>нет в принципе!</b></i>❌</b>", parse_mode="HTML")
        else:
            await msg.answer(f"<b>❌Пользователь с id: <u>{usr}</u> не найден!❌</b>", parse_mode="HTML")
    else:
        await msg.reply("🔐<b><i>Извините, но у вас недостаточно прав для того чтобы использовать эту комманду!</i></b>🔐", parse_mode="HTML")

@dp.message_handler(commands="setstat")
async def setSat(msg: types.Message):
    totality_command(msg.from_user.id, "/setstat")
    if infadmin(msg.from_user.id):
        await msg.answer("<b><i>🗑Удаление данных статистики🗑</i></b>\n\n<i>При этом действии совершится полная очистка <b>ВСЕХ</b> данных статистики</i>\n\n<u>Вы дествительно хотите очистить данные?</u>", parse_mode="HTML", reply_markup=keyboard2)
    else:
        await msg.reply("🔐<b><i>Извините, но у вас недостаточно прав для того чтобы использовать эту комманду!</i></b>🔐", parse_mode="HTML")


@dp.message_handler(commands=["statistics", "stat"])
async  def statistics(msg: types.Message):
    totality_command(msg.from_user.id, "/statistics")
    write_json("statistics")
    await msg.answer("<b>✅Статистика загружается!!✅</b>", parse_mode='HTML')
    text = stat()
    await bot.edit_message_text(message_id=msg.message_id+1, chat_id=msg.chat.id, text=text, parse_mode="HTML")


@dp.message_handler(content_types = ["photo"])
async def dowphoto(message: types.Message):
    await message.photo[-1].download(destination_file=f'{message.from_user.id}.jpg')
    user_id = message.from_user.id
    js = requests.post("https://api.trace.moe/search",
                       data=open(f"{user_id}.jpg", "rb"),
                       headers={"Content-Type": "image/jpeg"}
                       ).json()
    result = f'''
<strong>✅Результат✅</strong>
<strong>📄Название:</strong> {js["result"][0]["filename"]}
<strong>🗂Эпизод:</strong> {js["result"][0]['episode']}
<strong>⏳Время:</strong> {time.strftime("%H:%M:%S", time.gmtime(js["result"][0]["from"]))} - {time.strftime("%H:%M:%S", time.gmtime(js["result"][0]["to"]))}
<strong>📈Слвпадение:</strong> {float(js["result"][0]["similarity"]) * 100}%
                       '''
    os.remove(f"{user_id}.jpg")
    await message.reply(result, parse_mode="HTMl")
    await bot.send_video(message.chat.id, js["result"][0]["video"])


@dp.message_handler(commands="animeframesearchbyphoto")
async def Search(message: types.Message):
    totality_command(message.from_user.id, "/animeframesearchbyphoto")
    write_json("animeframesearchbyphoto")
    await message.answer('Пришлите мне фото для поиска')
    async def searchbyphoto(message: types.Message):
        try:
            await dowphoto()
        except Exception:
            pass
    dp.register_message_handler(searchbyphoto)


@dp.message_handler(content_types="text")
async def echo_message(msg: types.Message):
    times = f"{datetime.now().day}_{datetime.now().month}_{datetime.now().year} ------ {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
    Last_Activity(f"{msg.from_user.id}", times)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)