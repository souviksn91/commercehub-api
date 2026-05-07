from rest_framework.throttling import AnonRateThrottle


# throttle for login endpoint
class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


# throttle for registration endpoint
class RegisterRateThrottle(AnonRateThrottle):
    scope = "register"