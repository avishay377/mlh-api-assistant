import asyncio
import os
from dotenv import load_dotenv
from backboard import BackboardClient

load_dotenv()

async def main():
    api_key = os.getenv("BACKBOARD_API_KEY")
    if not api_key:
        raise ValueError("BACKBOARD_API_KEY is missing from .env")

    client = BackboardClient(api_key=api_key)

    assistant = await client.create_assistant(
        name="Document Assistant",
        system_prompt="You are a helpful document analysis assistant"
    )

    document = await client.upload_document_to_assistant(
        assistant.assistant_id,
        "server/data/documents/cognito-dg-pages.pdf"
    )

    print("Waiting for document to be indexed...")

    while True:
        status = await client.get_document_status(document.document_id)

        if status.status == "indexed":
            print("Document indexed successfully!")
            break
        elif status.status == "failed":
            print(f"Document indexing failed: {status.status_message}")
            return

        await asyncio.sleep(2)

    thread = await client.create_thread(assistant.assistant_id)

    async for chunk in await client.add_message(
        thread_id=thread.thread_id,
        content="What are the key points in the uploaded document?",
        stream=True
    ):
        if chunk.get("type") == "content_streaming":
            c = chunk.get("content", "")
            if c:
                print(c, end="", flush=True)

    print()


if __name__ == "__main__":
    asyncio.run(main())