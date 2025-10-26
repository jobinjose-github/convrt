from utils.constants import file_types

class Utility:
    def __init__(self):
        self.file_types = file_types

    def get_service_type(self, source_file_type: str) -> str:
        source_file_type = source_file_type.lower()
        for service_type, file_types in self.file_types.items():
            for file_type in file_types:
                if file_type == source_file_type:
                    return service_type
        else:
            raise ValueError("Invalid File Type!!!")