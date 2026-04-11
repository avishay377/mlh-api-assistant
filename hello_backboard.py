import asyncio
import os
from backboard import BackboardClient
import dotenv

dotenv.load_dotenv()

async def main():
    client = BackboardClient(api_key=os.getenv("BACKBOARD_API_KEY"))

    assistant = await client.create_assistant(
        name="My First Assistant",
        system_prompt="You are a helpful assistant that responds concisely."
    )
    print(f"Created assistant: {assistant.assistant_id}")

    thread = await client.create_thread(assistant.assistant_id)
    print(f"Created thread: {thread.thread_id}")

    user_message = "say Hello World"
    print(f"You: {user_message}")

    response = await client.add_message(
        thread_id=thread.thread_id,
        content=user_message,
        stream=False
    )
    print(f"Assistant: {response.content}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise