import json
import os


class JsonStorage:
    file_path = "save.json"

    @staticmethod
    def set(key: str, value):
        data = JsonStorage.read_file()
        data[key] = value
        JsonStorage.write_file(data)

    @staticmethod
    def get(key: str, default=None):
        data = JsonStorage.read_file()
        try:
            return data[key]
        except KeyError:
            return default

    def read_file():
        if not JsonStorage.file_exists():
            JsonStorage.create_file()

        with open(JsonStorage.file_path, "r") as file:
            return json.load(file)

    def write_file(data):
        with open(JsonStorage.file_path, "w") as file:
            json.dump(data, file)

    def create_file():
        with open(JsonStorage.file_path, "w") as file:
            json.dump({}, file)

    def file_exists():
        return os.path.exists(JsonStorage.file_path)

