"""Constants and Enums for use in HSTSReaders."""


class Paths:
    """Location of HSTS databases."""

    class Windows:
        """Location of HSTS Files on Windows."""

        CHROME = r'Users\*\AppData\Roaming\Mozilla\Firefox\Profiles\*\SiteSecurityServiceState.txt'
        FIREFOX = r'Users\*\AppData\Local\Google\Chrome\User Data\TransportSecurity'

    class Linux:
        """Location of HSTS Files on Linux."""

        CHROME = 'home/*/.config/google-chrome*/Default/TransportSecurity'
        FIREFOX = 'home/*/.mozilla/firefox/*/SiteSecurityServiceState.txt'
