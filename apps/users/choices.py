PASSWORD_RESET_EMAIL_TITLE = "Password reset"
PASSWORD_RESET_EMAIL_MESSAGE = "A request has been received to reset the password for your account. \n" \
                               "Your new password: "


MANAGER = "MANAGER"
TEACHER = "TEACHER"
STUDENT = "STUDENT"


ROLE_CHOICES = [
    (MANAGER, MANAGER),
    (TEACHER, TEACHER),
    (STUDENT, STUDENT),
]


DEVICE_MOBILE = "MOBILE"
DEVICE_TABLET = "TABLET"
DEVICE_PC = "PC"
DEVICE_TYPE = [
    (DEVICE_MOBILE, DEVICE_MOBILE),
    (DEVICE_TABLET, DEVICE_TABLET),
    (DEVICE_PC, DEVICE_PC),
]
