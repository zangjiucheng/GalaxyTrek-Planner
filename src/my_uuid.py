import uuid


class UUIDManager:
    def __init__(self, version=4):
        """
        Initialize the UUIDManager with a specified UUID version.
        Supported versions: 1, 3, 4, 5
        """
        if version not in [1, 3, 4, 5]:
            raise ValueError(
                "Unsupported UUID version. Supported versions are: 1, 3, 4, 5."
            )
        self.version = version

    def generate(self, name=None, namespace=None):
        """
        Generate a UUID based on the specified version.
        For UUID1, no additional arguments are needed.
        For UUID3 and UUID5, both name and namespace are required.
        For UUID4, no additional arguments are needed.
        """
        if self.version == 1:
            return uuid.uuid1()
        elif self.version == 3:
            if name is None or namespace is None:
                raise ValueError("UUID3 requires both name and namespace.")
            return uuid.uuid3(namespace, name)
        elif self.version == 4:
            return uuid.uuid4()
        elif self.version == 5:
            if name is None or namespace is None:
                raise ValueError("UUID5 requires both name and namespace.")
            return uuid.uuid5(namespace, name)

    def validate(self, uuid_string):
        """
        Validate whether a given string is a valid UUID.
        """
        try:
            val = uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False


# Example usage:
if __name__ == "__main__":
    # Generate a UUID4
    uuid_manager = UUIDManager(version=4)
    uuid4 = uuid_manager.generate()
    print(f"Generated UUID4: {uuid4}")

    # Validate the generated UUID
    is_valid = uuid_manager.validate(str(uuid4))
    print(f"Is the generated UUID valid? {is_valid}")

    # Generate a UUID1
    uuid_manager_v1 = UUIDManager(version=1)
    uuid1 = uuid_manager_v1.generate()
    print(f"Generated UUID1: {uuid1}")

    # Generate a UUID3
    uuid_manager_v3 = UUIDManager(version=3)
    namespace = uuid.NAMESPACE_DNS
    name = "example.com"
    uuid3 = uuid_manager_v3.generate(name=name, namespace=namespace)
    print(f"Generated UUID3: {uuid3}")

    # Generate a UUID5
    uuid_manager_v5 = UUIDManager(version=5)
    namespace = uuid.NAMESPACE_DNS
    name = "example.com"
    uuid5 = uuid_manager_v5.generate(name=name, namespace=namespace)
    uuid5_2 = uuid_manager_v5.generate(name=name, namespace=namespace)
    print(f"Generated UUID5: {uuid5}")
