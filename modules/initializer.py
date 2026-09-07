from configparser import ConfigParser, ExtendedInterpolation, NoSectionError
cfg = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)

def config_file():
    print("No config file found. Creating one.")
    debug = input("Do you want this to be a protyping session? (y/N)")
    debug = True if debug in ('y', 'Y') else False
    with open("./modules/config.cfg", "w", encoding="utf-8") as file:
        template = f"""[Main]
debugging = {debug}
"""
        file.write(template)    