# Copyright (C) 2021-2025 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

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
                uploader,
                views,
                upload_date,
            ) = await YouTube.details(url)
            if not title:
                return await mystic.edit_text(_["song_3"])
            if str(duration_min) == "None":
                return await mystic.edit_text(_["song_3"])
            if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
                )
            buttons = song_markup(_, vidid)
            await mystic.delete()
            caption = _["song_4"].format(
                title=title,
                uploader=uploader,
                duration=duration_min,
                views=views,
                upload_date=upload_date
            )
            return await message.reply_photo(
                thumbnail,
                caption=caption,
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
                uploader,
                views,
                upload_date,
            ) = await YouTube.details(query)
            if not title:
                return await mystic.edit_text(_["song_3"])
            if str(duration_min) == "None":
                return await mystic.edit_text(_["song_3"])
            if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
                )
            buttons = song_markup(_, vidid)
            await mystic.delete()
            caption = _["song_4"].format(
                title=title,
                uploader=uploader,
                duration=duration_min,
                views=views,
                upload_date=upload_date
            )
            return await message.reply_photo(
                thumbnail,
                caption=caption,
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
                return await CallbackQuery.edit_message_text(_["song_7"].format("No audio formats available"))
        except Exception as e:
            return await CallbackQuery.edit_message_text(_["song_7"].format(str(e)))
        keyboard = InlineKeyboard()
        quality_options = [
            {"format_id": "140", "label": "High Quality (256kbps)", "ext": "mp3"},
            {"format_id": "139", "label": "Medium Quality (128kbps)", "ext": "mp3"},
            {"format_id": "251", "label": "Low Quality (64kbps)", "ext": "mp3"},
        ]
        for option in quality_options:
            for x in formats_available:
                if x["format_id"] == option["format_id"] and x["ext"] == "mp3":
                    sz = convert_bytes(x["filesize"]) if x["filesize"] else "Unknown Size"
                    keyboard.row(
                        InlineKeyboardButton(
                            text=f"{option['label']} = {sz}",
                            callback_data=f"song_download {stype}|{option['format_id']}|{vidid}",
                        ),
                    )
                    break
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
                return await CallbackQuery.edit_message_text(_["song_7"].format("No video formats available"))
        except Exception as e:
            return await CallbackQuery.edit_message_text(_["song_7"].format(str(e)))
        keyboard = InlineKeyboard()
        quality_options = [
            {"format_id": "137", "label": "High Quality (1080p)", "ext": "mp4"},
            {"format_id": "136", "label": "Medium Quality (720p)", "ext": "mp4"},
            {"format_id": "134", "label": "Low Quality (360p)", "ext": "mp4"},
        ]
        for option in quality_options:
            for x in formats_available:
                if x["format_id"] == option["format_id"] and x["ext"] == "mp4":
                    sz = convert_bytes(x["filesize"]) if x["filesize"] else "Unknown Size"
                    keyboard.row(
                        InlineKeyboardButton(
                            text=f"{option['label']} = {sz}",
                            callback_data=f"song_download {stype}|{option['format_id']}|{vidid}",
                        ),
                    )
                    break
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
        title, duration_min, duration_sec, thumbnail, vidid, uploader, views, upload_date = await YouTube.details(yturl)
        if not title:
            return await mystic.edit_text(_["song_9"].format("Failed to fetch video details"))
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(str(e)))
    thumb_image_path = await CallbackQuery.message.download()
    caption = _["song_4"].format(
        title=title,
        uploader=uploader,
        duration=duration_min,
        views=views,
        upload_date=upload_date
    )
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
            caption=caption,
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
            caption=caption,
            thumb=thumb_image_path,
            title=title,
            performer=uploader,
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
