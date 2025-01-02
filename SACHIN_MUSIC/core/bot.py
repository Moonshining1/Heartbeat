from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
import config

from ..logging import LOGGER


class SACHIN(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="SACHIN_MUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.me = await self.get_me()
        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )
        except errors.ChannelInvalid:
            LOGGER(__name__).error(
                "Bot failed to access the log group/channel. Ensure the bot is added to your log group/channel."
            )
            exit()
        except errors.PeerIdInvalid:
            LOGGER(__name__).error(
                "Bot failed to access the log group/channel. Check the LOGGER_ID in your config."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot failed to access the log group/channel. Reason: {type(ex).__name__}."
            )
            exit()

        try:
            member_status = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member_status.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as an admin in your log group/channel."
                )
                exit()
        except errors.ChatAdminRequired:
            LOGGER(__name__).error(
                "Bot cannot verify admin status. Please ensure the bot is an admin in the log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Error while checking bot's admin status. Reason: {type(ex).__name__}."
            )
            exit()

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Bot...")
        await super().stop()
        LOGGER(__name__).info("Bot stopped successfully.")
