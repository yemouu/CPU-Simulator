from collections import defaultdict
from collections.abc import Sequence
from typing import override

from .resource import Resource


class ResourceManager:
    """Handles interactions between processes and resources

    Contains a list of resources and gives processes the ability to
    request and release resources by their resource id.
    """

    def __init__(self, resource_list: tuple[Resource, ...]):
        self._resource_list: tuple[Resource, ...] = resource_list

    def request(self, resource_id: int, process_id: int) -> bool:
        """Request a resource"""
        for resource in self._resource_list:
            if resource_id == resource.rid:
                if resource.available:
                    resource.toggle_availability(process_id)
                    return True
                else:
                    return False

        raise ValueError("Resource doesn't exist")

    def release(self, resource_id: int, process_id: int) -> None:
        """Release a resource"""
        for resource in self._resource_list:
            if resource_id == resource.rid and not resource.available:
                if process_id is resource.process_id:
                    resource.toggle_availability(None)


class ResourceAllocationGraph(ResourceManager):
    """A ResourceManager with the ability to detect deadlocks

    Deadlock detection is done using a Resource Allocation Graph and
    detecting a cycle within this graph.
    """

    def __init__(self, resource_list: tuple[Resource, ...]):
        super().__init__(resource_list)
        self._rag: dict[int | Resource, set[int | Resource]] = {}

    def _add_edge(
        self,
        key: int | Resource,
        value: int | Resource,
        graph: dict[int | Resource, set[int | Resource]] | None = None,
    ) -> None:
        """Helper function to add an edge to a graph

        Because 'value' of the graph is a set, we cannot simply use the
        `=` operator and because a 'key' nay not yet be in the
        dictionary, we cannot always use the `.add()` method of set.
        This method do the correct set of actions to ensure the graph
        is consistent while keeping this code in one place rather than
        duplicating to everywhere we may need to add an edge.
        """
        graph = self._rag if graph is None else graph
        if key in graph:
            graph[key].add(value)
            if value not in graph:
                graph[value] = set([])
        else:
            graph[key] = set([value])
            if value not in graph:
                graph[value] = set([])

    def _has_cycle(
        self,
        node: int | Resource,
        visited: dict[int | Resource, bool],
        stack: dict[int | Resource, bool],
        graph: dict[int | Resource, set[int | Resource]] | None = None,
    ) -> bool:
        """Detect cycles in a graph

        This algorithm uses depth-first search in order to detect a
        cycle in the graph.
        """
        graph = self._rag if graph is None else graph

        visited[node] = True
        stack[node] = True

        for adjacent in graph[node]:
            if not visited[adjacent]:
                if self._has_cycle(adjacent, visited, stack, graph):
                    return True
            elif stack[adjacent]:
                return True

        stack[node] = False
        return False

    def is_deadlocked(self, graph: dict[int | Resource, set[int | Resource]] | None = None) -> bool:
        """Detect a resource allocation graph in a deadlocked state

        This runs our cycle detection starting from each node in the
        graph. If there is even one cycle, we are deadlocked.
        """
        graph = self._rag if graph is None else graph

        visited: dict[int | Resource, bool] = defaultdict(bool)
        stack: dict[int | Resource, bool] = defaultdict(bool)

        for node in graph:
            if not visited[node]:
                if self._has_cycle(node, visited, stack, graph):
                    return True

        return False

    @override
    def request(self, resource_id: int, process_id: int) -> bool:
        """Request a resource

        When we request a resource we make sure to update the resource
        allocation graph.
        """
        for resource in self._resource_list:
            if resource_id == resource.rid:
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
        """Release a resource

        When we release a resource we make sure to update the resource
        allocation graph.
        """
        for resource in self._resource_list:
            if resource_id == resource.rid and not resource.available:
                if process_id is resource.process_id:
                    resource.toggle_availability(process_id)
                    self._rag[resource].remove(process_id)


class AvoidantResourceAllocationGraph(ResourceAllocationGraph):
    """A ResourceManager with the ability to avoid deadlocks"""

    def __init__(self, resource_list: tuple[Resource, ...]):
        super().__init__(resource_list)

    def add_process_claims(self, process_id: int, resource_ids: Sequence[int]):
        """Add process to resource relations to the allocation graph"""
        for resource_id in resource_ids:
            for resource in self._resource_list:
                if resource_id == resource.rid:
                    self._add_edge(process_id, resource)

    def remove_process_claims(self, process_id: int):
        """Remove a process from the allocation graph"""
        self._rag.pop(process_id, None)

    # A deepcopy makes a copy of the Resource objects as well which
    # prevents us from finding the Resource object we want
    def _copy_rag(self) -> dict[int | Resource, set[int | Resource]]:
        """Create a copy of the resource allocation graph"""
        temp_rag: dict[int | Resource, set[int | Resource]] = {}
        for key in self._rag:
            for value in self._rag[key]:
                self._add_edge(key, value, temp_rag)

        return temp_rag

    @override
    def request(self, resource_id: int, process_id: int) -> bool:
        """Request a resource

        When we request a resource we check to make sure that the
        request wont cause a deadlock.
        """
        for resource in self._resource_list:
            if resource_id == resource.rid:
                temp_rag = self._copy_rag()
                temp_rag[process_id].remove(resource)
                self._add_edge(resource, process_id, temp_rag)
                deadlocked: bool = self.is_deadlocked(temp_rag)

                if resource.available and not deadlocked:
                    resource.toggle_availability(process_id)
                    self._rag[process_id].remove(resource)
                    self._add_edge(resource, process_id)
                    return True
                else:
                    print("Avoided Deadlock") if deadlocked else None
                    return False
        raise ValueError("Resource doesn't exist")

    @override
    def release(self, resource_id: int, process_id: int) -> None:
        """Release a resource

        When we release a resource we make sure to update the resource
        allocation graph.
        """
        for resource in self._resource_list:
            if resource_id == resource.rid and not resource.available:
                if process_id is resource.process_id:
                    resource.toggle_availability(process_id)
                    self._add_edge(process_id, resource)
                    self._rag[resource].remove(process_id)
