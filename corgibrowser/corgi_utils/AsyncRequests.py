import aiohttp
import asyncio

class AsyncRequests:
    async def get_response(self, url):
        """Asynchronous method to get a response using aiohttp."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                text = await response.text()
                status_code = response.status
                return text, status_code