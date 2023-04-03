from ttkbootstrap.dialogs.dialogs import Messagebox
from constants.popups import *
from jsonschema import validate
import toml

SETTINGS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "RADAR": {
            "type": "object",
            "properties": {
                "ENABLED": {"type": "integer", "minimum": 0, "maximum": 1}
            },
            "required": ["ENABLED"]
        },
        "TRIGGER_BOT": {
            "type": "object",
            "properties": {
                "ENABLED": {"type": "integer", "minimum": 0, "maximum": 1}
            },
            "required": ["ENABLED"]
        },
        "BHOP": {
            "type": "object",
            "properties": {
                "ENABLED": {"type": "integer", "minimum": 0, "maximum": 1}
            },
            "required": ["ENABLED"]
        },
        "ESP": {
            "type": "object",
            "properties": {
                "ENABLED": {"type": "integer", "minimum": 0, "maximum": 1},
                "ENEMY_COLOR": {"type": "array", "items": {"type": "integer", "minimum": 0, "maximum": 255}, "minItems": 3, "maxItems": 3},
                "OPACITY": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            "required": ["ENABLED"]
        },
        "FLASH": {
            "type": "object",
            "properties": {
                "ENABLED": {"type": "integer", "minimum": 0, "maximum": 1},
                "VALUE": {"type": "number", "minimum": 0.0, "maximum": 100.0}
            },
            "required": ["ENABLED", "VALUE"]
        },
        "FOV": {
            "type": "object",
            "properties": {
                "ENABLED": {"type": "integer", "minimum": 0, "maximum": 1},
                "VALUE": {"type": "number", "minimum": 0.0, "maximum": 100.0}
            },
            "required": ["ENABLED", "VALUE"]
        }
    },
    "required": ["RADAR", "TRIGGER_BOT", "BHOP", "ESP", "FLASH", "FOV"]
}


class Config:
    def __init__(self) -> None:
        self.user_config = self.load()

    def load():
        data = {}
        try:
            with open("config.toml", "r", encoding="utf-8") as fd:
                content = fd.read()
                data = toml.loads(content)
            try:
                validate(
                    instance=data,
                    schema=SETTINGS_SCHEMA,
                )
            except:
                Messagebox.show_error(POP_CFG_PARSE_ERR, title="Error")
                exit(1)

            return data
        except Exception as err:
            Messagebox.show_error(POP_CFG_LOCAT_ERR, title="Error")
            exit(1)

    def save():
        try:
            validate(
                instance=UserConfig,
                schema=SETTINGS_SCHEMA,
            )
            try:
                with open("config.toml", "w", encoding="utf-8") as fd:
                    fd.write(toml.dumps(UserConfig))
                    Messagebox.show_info(POP_CFG_SUC, title="Success")

            except Exception as err:
                Messagebox.show_error(POP_CFG_SAVE_ERR, title="Error")

        except:
            Messagebox.show_error(POP_CFG_PARSE_ERR, title="Error")


UserConfig = Config.load()


def Toggle(service_key: str, field="ENABLED"):
    is_enabled = bool(UserConfig[service_key][field])
    UserConfig[service_key][field] = int(not is_enabled)
