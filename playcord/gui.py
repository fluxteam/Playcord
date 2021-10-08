from typing import Optional
import toga
import toga.style
from toga.style.pack import Pack
from travertino.constants import BOLD, COLUMN, MONOSPACE, ROW, SANS_SERIF
from playcord.config import Configuration
from playcord.classes import Constants
from playcord.account import Account
import webbrowser
import sys
import os
import traceback
from urllib.parse import urlparse, parse_qs
from pypresence import Presence
import time
import asyncio

class Playcord(toga.App):
    # Current signed in account.
    account = None

    # Current signed account ID.
    account_id = None

    @staticmethod
    def on_account_select(select : toga.Selection):
        """
        Handler for account selection.
        """
        if not select.app:
            # Somehow running refresh_account_list() method triggers on_account_select()
            # and passes "app" attribute None, so this ignores it.
            pass
        elif (select.value in select.items) and (select.value != select.items[0]):
            # Check if already signed in, because there is no point in
            # creating a new connection if account is already signed in.
            if Playcord.account_id != select.value:
                select.app.login_account(select.value)
        else:
            Playcord.account = None
            Playcord.account_id = None
            select.app.refresh_profile()


    @staticmethod
    def on_account_delete(button : toga.Button):
        """
        Handler for account deletion.
        """
        account = Configuration.get_account(button.app.account_label.text)
        if account:
            Configuration.delete_account(account.id)
            button.app.refresh_account_list()
        else:
            button.app.main_window.error_dialog("Invalid account", "This is not a valid account so it can't be deleted.")


    @staticmethod
    def on_account_add(button : toga.Button):
        """
        Handler for account add. Opens a URL so user can login with their own credentials.
        """
        button.app.main_window.info_dialog("Info", "Playcord will close and authorization window will be launched on your browser to login with your account. After signing in, select 'Playcord' when it asks for selecting an application.")
        webbrowser.open(Constants.LOGIN_URL)
        button.app.main_window.close()
        button.app.exit()


    def refresh_account_list(self):
        """
        Refreshes the account list selection.
        """
        self.account_selection.items = ["Select account...", *[x.id for x in Configuration.list_account()]]


    def import_account(self, code : str):
        """
        Imports an account by authorization code.
        """
        Playcord.account = Account.login(code)
        self.refresh_profile()
        self.main_window.info_dialog("Import successful", f"Added account successfully!")
        self.refresh_account_list()

    
    def login_account(self, id : str):
        """
        Login with account ID.
        """
        self.status_label.text = "Signing in..."
        Playcord.account = Account.login_refresh(Configuration.get_account(id).token or "")
        self.refresh_profile()

    
    def refresh_profile(self):
        """
        Displays the current game status.
        """
        if Playcord.account:
            if Playcord.account.needs_refresh:
                Playcord.account.refresh()
            profile = Playcord.account.profile()
            Configuration.set_account(profile.id, {
                "token": Playcord.account.session.refresh_token
            })
            Playcord.account_id = profile.id
            self.status_label.text = "Online" if profile.online else "Offline"
            self.game_label.text = "No any game running." if not profile.game else profile.game.name
            self.account_image.image = toga.Image(profile.avatar_url)
            self.account_label.text = profile.id
        else:
            self.account_label.text = "No account has selected."
            self.status_label.text = ""
            self.game_label.text = ""
            self.account_image.image = toga.Image(Constants.DEFAULT_AVATAR_URL)


    def handle_uri(self):
        """
        Handles the URI parameters and executes `import_account()` if an account login has detected.
        """
        # If app launched with com.playstation.playstationapp:// parameter,
        # parse URL and add account.
        if (len(sys.argv) == 2) and sys.argv[1].startswith("com.playstation.playstationapp://"):
            # Get code from URL.
            code = parse_qs(urlparse(sys.argv[1]).query).get("code", [None])[0]
            # Import account if code is provided.
            if not code:
                self.main_window.info_dialog("Importing account failed", "Looks like an URL handler triggered, however there is no authorization code in the URL. Skipping the import.")
            else:
                self.import_account(code)

    
    def send_discord_rpc(self):
        """
        Sends PlayStation status to Discord.
        """
        if self.discord_enable.is_on:
            if self.rpc.sock_writer == None:
                self.rpc.connect()
            if self.account:
                self.rpc.update(
                    details = self.account.id,
                    state = self.game_label.text or None,
                    large_text = "Playcord",
                    large_image = "logo.png",
                    start = self.current_time
                )
            else:
                self.rpc.update(
                    details = "Idle",
                    large_text = "Playcord",
                    large_image = "logo.png",
                    start = self.current_time
                )
        else:
            if self.rpc.sock_writer != None:
                self.rpc.close()

    
    async def update_discord(self):
        await asyncio.sleep(5)
        while True:
            self.refresh_profile()
            self.send_discord_rpc()
            await asyncio.sleep(15)


    def startup(self):
        self.main_window = toga.MainWindow(
            title = self.name, 
            size = (500, 230),
            resizeable = False
        )
        self.rpc = Presence(Constants.DISCORD_CLIENT_ID)
        self.current_time = int(time.time())
        self.account_label = toga.Label("No account has selected.", style = Pack(font_size = 10, font_family = SANS_SERIF, font_weight = BOLD))
        self.status_label = toga.Label("", style = Pack(font_size = 10, font_family = SANS_SERIF))
        self.game_label = toga.Label("", style = Pack(font_size = 10, font_family = SANS_SERIF))
        self.account_selection = toga.Selection(items = [], on_select = self.on_account_select, style = Pack(font_size = 10, font_family = SANS_SERIF, flex = 1, padding_right = 10))
        self.account_image = toga.ImageView(toga.Image(Constants.DEFAULT_AVATAR_URL), style = Pack(width = 60, height = 60, padding_right = 15))
        self.discord_enable = toga.Switch("Connect to Discord", style = Pack(font_size = 10, font_family = SANS_SERIF), on_toggle = self.discord_rpc)
        self.refresh_account_list()
        self.handle_uri()
        self.main_window.content = toga.Box(
            children = [
                toga.Box(style = Pack(direction = ROW, padding_bottom = 10), children = [
                    self.account_selection,
                    toga.Button("Add", style = Pack(font_size = 10, font_family = SANS_SERIF, padding_right = 10), on_press = self.on_account_add),
                    toga.Button("Remove", style = Pack(font_size = 10, font_family = SANS_SERIF), on_press = self.on_account_delete)
                ]),
                toga.Box(style = Pack(direction = ROW, padding_bottom = 20), children = [
                    self.account_image,
                    toga.Box(style = Pack(direction = COLUMN), children = [
                        self.account_label,
                        self.status_label,
                        self.game_label
                    ])
                ]),
                self.discord_enable
            ], 
            style = Pack(direction = COLUMN, padding = 20, font_family = MONOSPACE)
        )
        # Run forever.
        asyncio.run(self.update_discord())
        # Show the main window
        self.main_window.show()

def main():
    return Playcord(
        'Playcord', 
        'com.ysfchn.playcord',
        'Playcord',
        author = "Yusuf Cihan",
        description = "Show your Playstation status as Discord rich presence.",
        home_page = "https://github.com/ysfchn/Playcord"
    )
