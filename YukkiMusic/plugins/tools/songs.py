import os
from pykeyboard import InlineKeyboard
from pyrogram import enums, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)
from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from YukkiMusic import YouTube, app
from YukkiMusic.utils.decorators.language import language, languageCB
from YukkiMusic.utils.formatters import convert_bytes
from YukkiMusic.utils.inline.song import song_markup

@app.on_message(filters.command("song") & ~BANNED_USERS)
@language
async def song(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        try:
            (
                title,
                duration_min,
                duration_sec,
                thumbnail,
                vidid,
            ) = await YouTube.details(url)
            if not title:  # Check if details fetch failed
                return await mystic.edit_text(_["song_3"])
            if str(duration_min) == "None":
                return await mystic.edit_text(_["song_3"])
            if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
                )
            buttons = song_markup(_, vidid)
            await mystic.delete()
            return await message.reply_photo(
                thumbnail,
                caption=_["song_4"].format(title),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except Exception as e:
            return await mystic.edit_text(_["song_3"].format(str(e)))
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
        mystic = await message.reply_text(_["play_1"])
        query = message.text.split(None, 1)[1]
        try:
            (
                title,
                duration_min,
                duration_sec,
                thumbnail,
                vidid,
            ) = await YouTube.details(query)
            if not title:  # Check if details fetch failed
                return await mystic.edit_text(_["song_3"])
            if str(duration_min) == "None":
                return await mystic.edit_text(_["song_3"])
            if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
                )
            buttons = song_markup(_, vidid)
            await mystic.delete()
            return await message.reply_photo(
                thumbnail,
                caption=_["song_4"].format(title),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except Exception as e:
            return await mystic.edit_text(_["play_3"].format(str(e)))

@app.on_callback_query(filters.regex(pattern=r"song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(pattern=r"song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass
    if stype == "audio":
        try:
            formats_available, link = await YouTube.formats(vidid, True)
            if not formats_available:
                return await CallbackQuery.edit_message_text(_["song_7"].format("No formats available"))
        except Exception as e:
            return await CallbackQuery.edit_message_text(_["song_7"].format(str(e)))
        keyboard = InlineKeyboard()
        done = []
        for x in formats_available:
            if x["ext"] == "mp3"  # Only allow mp3 and m4a formats
                continue
            form = x.get("format_note", "Unknown").title()
            sz = convert_bytes(x["filesize"]) if x["filesize"] else "Unknown Size"
            if form in done:
                continue
            done.append(form)
            fom = x["format_id"]
            keyboard.row(
                InlineKeyboardButton(
                    text=f"{form} Audio = {sz}",
                    callback_data=f"song_download {stype}|{fom}|{vidid}",
                ),
            )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
        )
        return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
    else:
        try:
            formats_available, link = await YouTube.formats(vidid, True)
            if not formats_available:
                return await CallbackQuery.edit_message_text(_["song_7"].format("No formats available"))
        except Exception as e:
            return await CallbackQuery.edit_message_text(_["song_7"].format(str(e)))
        keyboard = InlineKeyboard()
        done = ["160", "133", "134", "135", "136", "137", "298", "299", "264", "304", "266", "bestvideo[height<=720]+bestaudio"]
        for x in formats_available:
            if x["ext"] == "mp4":  # Restrict to video formats
                continue
            if x["format_id"] not in done:
                continue
            sz = convert_bytes(x["filesize"]) if x["filesize"] else "Unknown Size"
            ap = x.get("format_note", "Unknown")
            to = f"{ap} = {sz}"
            keyboard.row(
                InlineKeyboardButton(
                    text=to,
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            )
        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
        )
        return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)

@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading")
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(yturl)
        if not title:
            return await mystic.edit_text(_["song_9"].format("Failed to fetch video details"))
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(str(e)))
    thumb_image_path = await CallbackQuery.message.download()
    if stype == "video":
        width = CallbackQuery.message.photo.width if CallbackQuery.message.photo else 1280
        height = CallbackQuery.message.photo.height if CallbackQuery.message.photo else 720
        file_path = await YouTube.download(
            yturl, mystic, songvideo=True, format_id=format_id, title=title
        )
        if not file_path:
            return await mystic.edit_text(_["song_9"].format("Download failed"))
        med = InputMediaVideo(
            media=file_path,
            duration=duration_sec,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            return await mystic.edit_text(_["song_10"].format(str(e)))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(thumb_image_path):
                os.remove(thumb_image_path)
    elif stype == "audio":
        file_path = await YouTube.download(
            yturl,
            mystic,
            songaudio=True,
            format_id=format_id,
            title=title,
        )
        if not file_path:
            return await mystic.edit_text(_["song_9"].format("Download failed"))
        med = InputMediaAudio(
            media=file_path,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=vidid,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_AUDIO,
        )
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            return await mystic.edit_text(_["song_10"].format(str(e)))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(thumb_image_path):
                os.remove(thumb_image_path)
