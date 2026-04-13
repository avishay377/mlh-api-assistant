import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from app.services.assistant_service import (
    ask_assistant,
    create_document_assistant,
    upload_document_to_assistant,
    wait_for_document_indexing,
)

load_dotenv()

DOCUMENT_PATH = "data/documents/cognito-dg-pages.pdf"
QUESTION = "What are the key points in the uploaded document?"


async def main():
    assistant = await create_document_assistant()

    document = await upload_document_to_assistant(
        assistant.assistant_id,
        DOCUMENT_PATH,
    )

    print("Waiting for document to be indexed...")
    await wait_for_document_indexing(document.document_id)
    print("Document indexed successfully!")

    answer = await ask_assistant(
        assistant.assistant_id,
        QUESTION,
    )

    print("\nAssistant answer:\n")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())