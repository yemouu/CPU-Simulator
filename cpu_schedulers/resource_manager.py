from .resource import Resource


class ResourceManager:
    def __init__(self, resource_list: tuple[Resource]):
        self._resource_list: tuple[Resource] = resource_list

    def request(self, resource_id: int, process_id: int) -> bool:
        for resource in self._resource_list:
            if resource_id == resource.r_id and resource.available:
                resource.toggle_availability(process_id)
                return True

        return False

    def release(self, resource_id: int, process_id: int) -> None:
        for resource in self._resource_list:
            if resource_id == resource.r_id and not resource.available:
                if process_id == resource.process_id:
                    resource.toggle_availability(process_id)
