from urllib.parse import urlencode

def get_login_url():
    return "https://ca.account.sony.com/api/v1/oauth/authorize" + "?" + \
        urlencode({
            "service_entity": "urn:service-entity:psn",
            "response_type": "code",
            "client_id": "ac8d161a-d966-4728-b0ea-ffec22f69edc",
            "redirect_uri": "com.playstation.PlayStationApp://redirect",
            "scope": "psn:clientapp referenceDataService:countryConfig.read",
            "request_locale": "en_US",
            "ui": "pr",
            "service_logo": "ps",
            "layout_type": "popup",
            "smcid": "remoteplay",
            "prompt": "always",
            "PlatformPrivacyWs1": ""
        }).replace('+', '%20')