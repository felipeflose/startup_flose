import asyncio
from typing import Dict, List, Callable, Awaitable
from collections import defaultdict
from flose.core.models import FLOSEMessage
from flose.core.enums import PriorityLevel

MessageHandler = Callable[[FLOSEMessage], Awaitable[None]]

class EventBus:
    """Async Priority Event Bus for Multi-Agent Communication."""

    def __init__(self):
        self._subscribers: Dict[str, List[MessageHandler]] = defaultdict(list)
        # Priority Queues: index 0 (Critical) to 3 (Low)
        self._queues: Dict[PriorityLevel, asyncio.Queue] = {
            level: asyncio.Queue() for level in PriorityLevel
        }
        self._is_running = False
        self._worker_task: asyncio.Task | None = None

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        """Subscribe a handler to a specific topic."""
        self._subscribers[topic].append(handler)

    async def publish(self, message: FLOSEMessage) -> None:
        """Publish a message to the appropriate priority queue."""
        queue = self._queues.get(message.priority, self._queues[PriorityLevel.MEDIUM])
        await queue.put(message)

    async def start(self) -> None:
        """Start the background event dispatcher loop."""
        self._is_running = True
        self._worker_task = asyncio.create_task(self._dispatch_loop())

    async def stop(self) -> None:
        """Stop the background event dispatcher loop."""
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def _dispatch_loop(self) -> None:
        """Process messages starting from highest priority (CRITICAL = 0)."""
        while self._is_running:
            message_processed = False
            for level in sorted(PriorityLevel, key=lambda x: x.value):
                queue = self._queues[level]
                if not queue.empty():
                    message: FLOSEMessage = await queue.get()
                    await self._deliver(message)
                    queue.task_done()
                    message_processed = True
                    break
            
            if not message_processed:
                await asyncio.sleep(0.01)

    async def _deliver(self, message: FLOSEMessage) -> None:
        """Deliver message to all subscribers of the message topic."""
        handlers = self._subscribers.get(message.topic, [])
        for handler in handlers:
            try:
                await handler(message)
            except Exception as e:
                # Log or handle exceptions gracefully
                print(f"[EventBus Error] Exception handling message {message.message_id}: {e}")
