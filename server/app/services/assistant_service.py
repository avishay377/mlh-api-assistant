import asyncio
from pathlib import Path

from app.integrations.backboard.client import get_backboard_client


DEFAULT_ASSISTANT_NAME = "Document Assistant"
DEFAULT_SYSTEM_PROMPT = "You are a helpful document analysis assistant"


async def create_document_assistant(
    name: str = DEFAULT_ASSISTANT_NAME,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
):
    client = get_backboard_client()
    assistant = await client.create_assistant(
        name=name,
        system_prompt=system_prompt,
    )
    return assistant


async def upload_document_to_assistant(assistant_id: str, document_path: str):
    client = get_backboard_client()

    path = Path(document_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")

    document = await client.upload_document_to_assistant(
        assistant_id,
        str(path),
    )
    return document


async def wait_for_document_indexing(document_id: str, poll_interval: int = 2):
    client = get_backboard_client()

    while True:
        status = await client.get_document_status(document_id)

        if status.status == "indexed":
            return status

        if status.status == "failed":
            raise RuntimeError(
                f"Document indexing failed: {status.status_message}"
            )

        await asyncio.sleep(poll_interval)


async def ask_assistant(assistant_id: str, content: str) -> str:
    client = get_backboard_client()

    thread = await client.create_thread(assistant_id)

    parts = []
    async for chunk in await client.add_message(
        thread_id=thread.thread_id,
        content=content,
        stream=True,
    ):
        if chunk.get("type") == "content_streaming":
            c = chunk.get("content", "")
            if c:
                parts.append(c)

    return "".join(parts)