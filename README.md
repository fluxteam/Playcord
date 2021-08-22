# Playcord

Shows your PlayStation status as Discord Rich Presence. Inspired and based by [Tustin's PlayStationDiscord](https://github.com/Tustin/PlayStationDiscord), but in Python.

> The project is still under development. It is tested on some platforms, however there is no guarantee about all platforms. If you get an error, please report by creating a new issue under "Issues" tab.

---

Playcord doesn't have a GNU/Linux build at the moment due to I don't have enough experience for making installable appplications in GNU/Linux but will be added as soon as possible.

## Story

One of my friends told me about an app that shows your PlayStation status as Discord Rich Presence, and he said that he was using Tustin's PlayStationDiscord app, but it was not connecting to Discord properly and causing login issues in the latest version.

Then I looked in GitHub to see alternatives, however surprisingly there is almost no any app that shows your current PlayStation game as rich presence on Discord. So I wanted to build an alternative in a different programming language that works cross-platform and without using Electron.

Tustin's PlayStationDiscord app uses Electron, so it can open the authorization URL in a new window and can control the browser window easily. As there is no something like this in Python, I thought about embedding a web driver in the application first, so it can launch a Chromium instance and control it in code. However, it caused a lot of issues when executing the compiled binary and increased the application size a lot. So I needed alternative solutions.

When you log in using PlayStation App's login URL, it opens the PlayStation App in the device by redirecting to `com.playstation.PlayStationApp://`, this is actually made for PlayStation's Android app, but other operating systems can handle such URIs too, for example in Windows, by modifying Registry. So it is possible to open a specified app when you go to that URI in your browser.

This is the best solution I found so far, so it is not needed to embed a browser instance and make the app bloated. Because of that Registry thing, the app must be installed on computer. So it is not portable. (Actually if you modify your Registry yourself then you can get it work but nobody wants to modify Registry manually.) However, I don't count this as a "disadvantage" because the app already creates and modifies files for storing your login tokens. So there is no point for making it portable.

## FAQ

#### Why it requires administrator permissions?

Actually, this is not required at all for such this app. However, modifying the Registry requires administrator permission. Also, the user can install to Program Files directory too. So this will cause exceptions in app and I don't know if there is a way to prevent installing application in system folders. So the app itself requires administrator permission too for keeping consistent.

#### Why my antivirus says that it is a malware?

False positive. There is nothing to say more. If you think it is a really "malware", then you might want to read the code. After all, you are using an open-source software. It is not possible to find a reason to worry about its safety.

### Why it doesn't have an GUI? Terminal is ugly.

I know. Playcord doesn't have a GUI because I don't want to import a ton of GUI libraries for only showing your avatar and name in app. It's only purpose is showing your PlayStation status on Discord. So if you want to close or disable it, you can just exit from app. And if you want to sign out, just delete the session file. But I can think about adding a _very-simple_ GUI if there are a lot of requests.

## Credits

Playcord wouldn't be possible without [PlayStationDiscord](https://github.com/Tustin/PlayStationDiscord). Also thanks to [@Venomliz](https://github.com/venomliz) for testing and giving suggestions in development phase of the app.

## Download

You can get it from ["Releases"](https://github.com/ysfchn/Playcord/releases) tab. You can also download it from ["Actions"](https://github.com/ysfchn/Playcord/actions).

## License

Source code is licensed under GPL 3.0 license. You must include the license notice in all copies or substantial uses of the work.
