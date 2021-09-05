from typing import List, Union
from readsettings import ReadSettings
from pathlib import Path

class ConfigurationAccount:
    """
    Represents an account saved in configuration.
    """

    def __init__(
        self,
        id : str,
        data : dict
    ) -> None:
        self.id : str = id
        self.token : str = data["token"]


class Configuration:
    """
    Manages the user accounts and stores configuration.
    """
    config = ReadSettings(str(Path.home().resolve() / "playcord.toml"))

    def __init__(self) -> None:
        pass
    
    @classmethod
    def list_account(cls) -> List[ConfigurationAccount]:
        """
        Lists the saved accounts and returns a list of `ConfigurationAccount` objects in the device.
        """
        accounts = []
        for x, y in cls.config.data.get("accounts", {}).items():
            try:
                account = ConfigurationAccount(x, y)
                accounts.append(account)
            except Exception:
                pass
        return accounts

    
    @classmethod
    def get_account(cls, id : str) -> Union[ConfigurationAccount, None]:
        """
        Gets a saved account, if account doesn't exists, Returns None.
        """
        return next((x for x in cls.list_account() if x.id == id), None)


    @classmethod
    def set_account(cls, id : str, data : dict) -> None:
        """
        Creates a account and saves it.
        """
        if "accounts" not in cls.config.data:
            cls.config.data["accounts"] = {}
        cls.config.data["accounts"][id] = data
        cls.config.save()


    @classmethod
    def delete_account(cls, id : str) -> None:
        """
        Deletes a saved account.
        """
        if id in cls.config.data.get("accounts", {}):
            del cls.config.data["accounts"][id]
        cls.config.save()