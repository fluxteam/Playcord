import time
from typing import Optional
from urllib.parse import urlencode

class Constants:
    """
    A class that holds auth endpoint, client token, login URL and others.
    """
    SCOPE = "psn:clientapp referenceDataService:countryConfig.read"
    REDIRECT_URI = "com.playstation.PlayStationApp://redirect"
    CLIENT_ID = "ac8d161a-d966-4728-b0ea-ffec22f69edc"
    AUTH_ENDPOINT = "https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token"
    LOGIN_ENDPOINT = "https://ca.account.sony.com/api/v1/oauth/authorize"
    CLIENT_TOKEN = "YWM4ZDE2MWEtZDk2Ni00NzI4LWIwZWEtZmZlYzIyZjY5ZWRjOkRFaXhFcVhYQ2RYZHdqMHY="
    DEFAULT_AVATAR_URL = "http://static-resource.np.community.playstation.net/avatar_xl/default/Defaultavatar_xl.png"
    
    LOGIN_URL = LOGIN_ENDPOINT + "?" + \
        urlencode({
            "service_entity": "urn:service-entity:psn",
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPE,
            "request_locale": "en_US",
            "ui": "pr",
            "service_logo": "ps",
            "layout_type": "popup",
            "smcid": "remoteplay",
            "prompt": "always",
            "PlatformPrivacyWs1": ""
        }).replace('+', '%20')


class Session:
    """
    A session object for storing OAuth responses.
    """
    def __init__(
        self,
        access_token : str,
        token_type : str,
        refresh_token : str,
        expires_in : str,
        scope : str = None
    ) -> None:
        self.access_token : str = access_token
        self.token_type : str = token_type
        self.refresh_token : str = refresh_token
        self.expires_in : int = int(expires_in or "0") or 3599
        self.scope : str = scope or Constants.SCOPE
        self._generated_time = int(time.time())

    @property
    def expire_seconds(self) -> int:
        """
        Returns how many seconds left for token refresh.
        """
        return (self._generated_time + self.expires_in) - int(time.time())


class Game:
    """
    Represents a game in profile.
    """
    def __init__(
        self,
        data : dict
    ) -> None:
        self.data : dict = data

    @property
    def name(self) -> Optional[str]:
        """
        Returns the name of the game that user is playing.
        Can be None if user is not playing right now.
        """
        return self.data.get("titleName", None)

    @property
    def image_url(self) -> Optional[str]:
        """
        Returns the image URL of the game that user is playing.
        Can be None if user is not playing right now.
        """
        return self.data.get("npTitleIconUrl", None)

    @property
    def id(self) -> Optional[str]:
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
        return any([self.name, self.id, self.image_url])

    def __bool__(self) -> bool:
        return self.playing

    def __eq__(self, o: object) -> bool:
        return \
            False if not isinstance(o, Game) else \
            any([o.id == self.id, o.image_url == self.image_url, o.name == self.name])

    def __str__(self) -> str:
        return self.name


class Profile:
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
        return self.data["avatarUrls"][0]["avatarUrl"]

    @property
    def id(self) -> str:
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
        Shortcut to: `profile.game.playing`
        """
        return bool(self.game)

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
        Can be None if user is not connected to PlayStation Network from a PlayStation device.
        """
        return self.data["presences"][0].get("platform", None)

    @property
    def game(self) -> Optional[Game]:
        """
        Returns the current game of the user, if user is not playing AND not connected to
        PlayStation Network from a PlayStation device, returns None.
        """
        return \
            None if len(self.data["presences"][0]) < 2 else \
            Game(self.data["presences"][0])

    def __bool__(self) -> bool:
        return self.online
    
    def __str__(self) -> str:
        return self.id