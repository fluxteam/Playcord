import time
from typing import Optional

class Session():
    """
    A session object for storing OAuth responses.
    """
    def __init__(
        self,
        access_token : str,
        token_type : str,
        refresh_token : str,
        expires_in : str,
        scope : str
    ) -> None:
        self.access_token : str = access_token
        self.token_type : str = token_type
        self.refresh_token : str = refresh_token
        self.expires_in : int = int(expires_in)
        self.scope : str = scope
        self._generated_time = int(time.time())

    @property
    def form_data(self) -> dict:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "redirect_uri": "com.playstation.PlayStationApp://redirect",
            "scope": self.scope
        }

    @property
    def left_seconds(self) -> int:
        """
        Returns how many seconds left for token refresh.
        """
        return (self._generated_time + self.expires_in) - int(time.time())


class Presence():
    """
    Represents a presence in profile.
    """
    def __init__(
        self,
        data : dict
    ) -> None:
        self.data : dict = data

    @property
    def platform(self) -> str:
        """
        Name of the platform that user is playing on.
        PSVITA, PS3, PS4...
        """
        return self.data["platform"]

    @property
    def game_name(self) -> Optional[str]:
        """
        Returns the name of the game that user is playing.
        Can be None if user is not playing right now.
        """
        return self.data.get("titleName", None)

    @property
    def game_url(self) -> Optional[str]:
        """
        Returns the image URL of the game that user is playing.
        Can be None if user is not playing right now.
        """
        return self.data.get("npTitleIconUrl", None)

    @property
    def game_id(self) -> Optional[str]:
        """
        Returns the ID of the game that user is playing.
        Can be None if user is not playing right now.
        """
        return self.data.get("npTitleId", None)

    @property
    def playing(self) -> bool:
        """
        Returns True if user is in the game. Otherwise, False.
        """
        return all([self.game_name, self.game_id, self.game_url])



class Profile():
    """
    An account profile that contains information about user.
    """
    def __init__(
        self,
        data : dict
    ) -> None:
        self.data : dict = data["profile"]

    @property
    def avatar_url(self) -> str:
        """
        Returns the avatar image URL of the account.
        """
        return self.data["avatarUrls"][0]

    @property
    def online_id(self) -> str:
        """
        Returns the user name of the account.
        """
        return self.data["onlineId"]

    @property
    def online(self) -> bool:
        """
        Returns True if user is online, else False.
        Online doesn't mean that user is playing a game right now, they can be online too by just
        connecting to PlayStation Network.
        """
        return self.data["primaryOnlineStatus"] == "online"

    @property
    def playing(self) -> bool:
        """
        Returns True if user is in the game. Otherwise, False.
        Shortcut to: `profile.presence.playing`
        """
        return False if not self.presence else self.presence.playing

    @property
    def plus(self) -> bool:
        """
        Returns True if user has PlayStation Plus subscription, else False.
        """
        return bool(self.data["plus"])

    @property
    def platform(self) -> Optional[str]:
        """
        Name of the platform that user is online on.
        """
        return None if not self.presence else self.presence.platform

    @property
    def presence(self) -> Optional[Presence]:
        """
        Returns the current presence of the user, if user is not playing AND not connected to
        PlayStation Network from a PlayStation device, returns None.
        """
        return \
            None if len(self.data["presences"][0]) < 2 else \
            Presence(self.data["presences"][0])