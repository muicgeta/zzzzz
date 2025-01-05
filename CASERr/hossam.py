from pyrogram import Client, filters
from pyrogram.raw.functions.phone import EditGroupCallParticipant as Edit, RequestCall
from pyrogram.raw.functions.phone import GetGroupCall
from pyrogram.raw.types import InputGroupCall
from pyrogram import filters, Client
import asyncio
import pyrogram
from typing import Optional
from pyrogram import Client, enums, filters
import pyrogram
from pyrogram import Client
import asyncio
from pyrogram import Client, idle
from random import randint
from typing import Optional
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, AlreadyJoinedError
from pyrogram.errors import ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError,AlreadyJoinedError)
from pyrogram.raw.base import GroupCallParticipant
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall, EditGroupCallParticipant
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat, InputUserSelf, GroupCallParticipant
from pyrogram.types import Message
import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.raw import types
from datetime import datetime
import requests
import pytz
from pyrogram.errors import ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant
from config import user, dev, call, logger, logger_mode, botname, appp
from CASERr.daty import get_call, get_userbot, get_dev, get_logger
from CASERr.CASERr import get_channel, devchannel, source, caes

mute_chattm = [] 
mute_chm = [] 
muded = [] 
speek = [] 

@Client.on_message(filters.text, group=20543565580)
async def mute_chattm54(c, message):
    hoss = await get_call(c.me.username)    
    hos = await get_userbot(c.me.username)    
    chat_id = message.chat.id
    if message.text == "تفعيل السماح بالتحدث":
        if chat_id in mute_chattm:
            await message.reply_text("السماح بالتحدث مفعل بالفعل في هذه المجموعة")
        else:
            vc = await get_group_call(hos, message, err_message="الكول مقفول")  # استخدم client بدلاً من user
            if not vc:
             await message.reply_text("الكول مقفول اصلا يليفه")
             return
            mute_chattm.append(chat_id)
            mute_chm.append(vc)
            await message.reply_text("تم تفعيل السماح بالتحدث بنجاح ✨♥")
    elif message.text == "تعطيل السماح بالتحدث":
        try:
           await hoss.leave_group_call(message.chat.id)
        except Exception as e:
            print(e)                     	
        if chat_id in mute_chattm:
            mute_chattm.remove(chat_id)
            mute_chm.clear()            
            muded.clear()
            await message.reply_text("تم تعطيل السماح بالتحدث بنجاح✨♥")
        else:
            await message.reply_text("السماح بالتحدث معطل بالفعل في هذه المجموعة")
            
async def get_group_call(
    client: Client, message: Message, err_message: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.reply_text(f"{err_message}")
    return False

async def mutegdv2d(bot_username):
    hoss = await get_call(bot_username)    
    hos = await get_userbot(bot_username)    
    app = appp[bot_username]    
    while True:
        for chat_id in mute_chattm:
            for vc in mute_chm:         
                try:
                    group_call = await hos.invoke(GetGroupCall(call=InputGroupCall(id=vc.id, access_hash=vc.access_hash), limit=100))
                    participants = group_call.participants
                    for participant in participants:
                        info = participant
                        if not info.muted:
                            mut = "يتحدث 🗣"
                        else:
                            mut = "ساكت 🔕"
                            try: 
                                if participant.peer.user_id not in muded:
                                    muded.append(participant.peer.user_id)  
                            except Exception as e:
                                print(e)                               
                    for hossamm in muded:
                        user = await hos.resolve_peer(hossamm)  
                        if not any(hossamm == participant.peer.user_id for participant in group_call.participants):
                            muded.remove(hossamm)
                        participant_info = next((p for p in group_call.participants if p.peer.user_id == hossamm), None)
                        if participant_info and participant_info.muted:
                          await hos.invoke(Edit(call=vc, participant=user, muted=False)) 
                          muded.remove(hossamm)                                                 
                except Exception as e:
                    print(e)              
        await asyncio.sleep(1)
    asyncio.create_task(mutegdv2d(bot_username))
    
@Client.on_message(filters.command(["mute", "unmute"]), group=8056)
async def mute_unmute(client, message):
    hos = await get_userbot(client.me.username)    
    command = message.command[0]
    user_id = int(message.command[1])
    mute_status = command == "mute"
    try:
        vc = await get_group_call(hos, message, err_message="الكول مقفول") 
        if not vc:
            await message.reply("الكول مقفول اصلا يليفه")
            return
        group_call = await hos.invoke(GetGroupCall(call=InputGroupCall(id=vc.id, access_hash=vc.access_hash), limit=100))        
        user = await hos.resolve_peer(user_id)
        if not any(participant.peer.user_id == user_id for participant in group_call.participants):
            await message.reply("المستخدم لم ينضم بعد إلى المكالمة الجماعية.")
            return
        await hos.invoke(Edit(call=vc, participant=user, muted=mute_status))
        await message.reply(f"تم {'كتم' if mute_status else 'إلغاء كتم'} المستخدم بنجاح.")  
    except Exception as e:
        print(f"حدث خطأ أثناء {'كتم' if mute_status else 'إلغاء كتم'} المستخدم: {e}")
