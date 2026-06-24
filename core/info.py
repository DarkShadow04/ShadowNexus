import platform


def get_platform():
    system = platform.system()

    if "Linux" in system:
        try:
            with open("/system/build.prop"):
                return "Android"
        except:
            return "Linux"

    return system
