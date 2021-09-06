This folder contains additional files that will be injected to Briefcase's cookiecutter templates. 

#### Why?

Because Briefcase doesn't have a configuration for adding URL/URI handlers. This is not acceptable for Playcord because Playcord requires registering `com.playstation.PlaystationApp://` URI handler to the system, so we download Briefcase's official templates and replace default files with these custom files.


* [Briefcase's .desktop file template](https://github.com/beeware/briefcase-linux-appimage-template/blob/1972003a82a72d86c3d993f05ad18cf74dbda992/%7B%7B%20cookiecutter.formal_name%20%7D%7D/%7B%7B%20cookiecutter.formal_name%20%7D%7D.AppDir/%7B%7B%20cookiecutter.bundle%20%7D%7D.%7B%7B%20cookiecutter.app_name%20%7D%7D.desktop)
* [Playcord's .desktop file template](linux/%7B%7B%20cookiecutter.bundle%20%7D%7D.%7B%7B%20cookiecutter.app_name%20%7D%7D.desktop)

* [Briefcase's .WXS file template](https://github.com/beeware/briefcase-windows-msi-template/blob/62da9d2b0f133532ed947a2c36043e039a90a184/%7B%7B%20cookiecutter.formal_name%20%7D%7D/%7B%7B%20cookiecutter.app_name%20%7D%7D.wxs)
* [Playcord's .WXS file template](windows/%7B%7B%20cookiecutter.app_name%20%7D%7D.wxs)