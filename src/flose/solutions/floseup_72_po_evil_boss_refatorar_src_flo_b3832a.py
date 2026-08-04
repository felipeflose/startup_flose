from typing import AsyncIterator, Protocol, runtime_checkable

class BackendProtocol(Protocol):
    async def fetch_data(self) -> AsyncIterator[str]:
        ...

@runtime_checkable
class AsyncTyping:
    def __init__(self, backend: BackendProtocol):
        self.backend = backend

    async def get_data(self) -> list[str]:
        return [item async for item in self.backend.fetch_data()]
