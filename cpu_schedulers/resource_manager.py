from collections import defaultdict
from collections.abc import Sequence
from typing import override

from .resource import Resource


class ResourceManager:
    def __init__(self, resource_list: tuple[Resource, ...]):
        self._resource_list: tuple[Resource, ...] = resource_list

    def request(self, resource_id: int, process_id: int) -> bool:
        for resource in self._resource_list:
            if resource_id == resource.r_id:
                if resource.available:
                    resource.toggle_availability(process_id)
                    return True
                else:
                    return False

        raise ValueError("Resource doesn't exist")

    def release(self, resource_id: int, process_id: int) -> None:
        for resource in self._resource_list:
            if resource_id == resource.r_id and not resource.available:
                if process_id is resource.process_id:
                    resource.toggle_availability(process_id)


class ResourceAllocationGraph(ResourceManager):
    def __init__(self, resource_list: tuple[Resource, ...]):
        super().__init__(resource_list)
        self._rag: dict[int | Resource, set[int | Resource]] = {}

    def _add_edge(
        self,
        key: int | Resource,
        value: int | Resource,
        graph: dict[int | Resource, set[int | Resource]] | None = None,
    ) -> None:
        graph = self._rag if graph is None else graph
        if key in graph:
            graph[key].add(value)
            if value not in graph:
                graph[value] = set([])
        else:
            graph[key] = set([value])
            if value not in graph:
                graph[value] = set([])

    def _detect_cycle(
        self,
        node: int | Resource,
        visited: dict[int | Resource, bool],
        stack: dict[int | Resource, bool],
        graph: dict[int | Resource, set[int | Resource]] | None = None,
    ) -> bool:
        graph = self._rag if graph is None else graph

        visited[node] = True
        stack[node] = True

        for adjacent in graph[node]:
            if not visited[adjacent]:
                if self._detect_cycle(adjacent, visited, stack, graph):
                    return True
            elif stack[adjacent]:
                return True

        stack[node] = False
        return False

    def detect_deadlock(self, graph: dict[int | Resource, set[int | Resource]] | None = None) -> bool:
        graph = self._rag if graph is None else graph

        visited: dict[int | Resource, bool] = defaultdict(bool)
        stack: dict[int | Resource, bool] = defaultdict(bool)

        for node in graph:
            if not visited[node]:
                if self._detect_cycle(node, visited, stack, graph):
                    return True

        return False

    @override
    def request(self, resource_id: int, process_id: int) -> bool:
        for resource in self._resource_list:
            if resource_id == resource.r_id:
                if resource.available:
                    resource.toggle_availability(process_id)
                    if process_id in self._rag and resource in self._rag[process_id]:
                        self._rag[process_id].remove(resource)
                    self._add_edge(resource, process_id)
                    return True
                else:
                    self._add_edge(process_id, resource)
                    return False
        raise ValueError("Resource doesn't exist")

    @override
    def release(self, resource_id: int, process_id: int) -> None:
        for resource in self._resource_list:
            if resource_id == resource.r_id and not resource.available:
                if process_id is resource.process_id:
                    resource.toggle_availability(process_id)
                    self._rag[resource].remove(process_id)


class AvoidantResourceAllocationGraph(ResourceAllocationGraph):
    def __init__(self, resource_list: tuple[Resource, ...]):
        super().__init__(resource_list)

    def add_process_claims(self, process_id: int, resource_ids: Sequence[int]):
        for resource_id in resource_ids:
            for resource in self._resource_list:
                if resource_id == resource.r_id:
                    self._add_edge(process_id, resource)

    def remove_process_claims(self, process_id: int):
        self._rag.pop(process_id, None)

    # A deepcopy makes a copy of the Resource objects as well which
    # prevents us from finding the Resource object we want
    def _create_temporary_rag(self) -> dict[int | Resource, set[int | Resource]]:
        temp_rag: dict[int | Resource, set[int | Resource]] = {}
        for key in self._rag:
            for value in self._rag[key]:
                self._add_edge(key, value, temp_rag)

        return temp_rag

    @override
    def request(self, resource_id: int, process_id: int) -> bool:
        for resource in self._resource_list:
            if resource_id == resource.r_id:
                temp_rag = self._create_temporary_rag()
                # if process_id in temp_rag and resource in temp_rag[process_id]:
                temp_rag[process_id].remove(resource)
                self._add_edge(resource, process_id, temp_rag)
                deadlocked: bool = self.detect_deadlock(temp_rag)

                if resource.available and not deadlocked:
                    resource.toggle_availability(process_id)
                    # if process_id in self._rag and resource in self._rag[process_id]:
                    self._rag[process_id].remove(resource)
                    self._add_edge(resource, process_id)
                    return True
                else:
                    print("Avoided Deadlock") if deadlocked else None
                    return False
        raise ValueError("Resource doesn't exist")

    @override
    def release(self, resource_id: int, process_id: int) -> None:
        for resource in self._resource_list:
            if resource_id == resource.r_id and not resource.available:
                if process_id is resource.process_id:
                    resource.toggle_availability(process_id)
                    self._add_edge(process_id, resource)
                    self._rag[resource].remove(process_id)
