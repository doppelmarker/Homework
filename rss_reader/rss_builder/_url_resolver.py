"""Module providing URL type resolving functionality."""
import asyncio
import logging
import platform
import re
from collections import namedtuple
from typing import List
from urllib.parse import urlparse

logger = logging.getLogger("rss-reader")

URL = namedtuple("URL", "item_num source")


class URLResolver:
    """Class which resolves types of the given URLs."""

    def __init__(self, all_urls: dict[int, set[str]], check_urls: bool):
        self.all_urls = all_urls
        self.check_urls = check_urls

    @staticmethod
    def _is_url_image_by_extension(url: str) -> bool:
        """Check if URL is an image by its extension."""
        image_extensions = (".png", ".jpeg", ".jpg")
        for image_extension in image_extensions:
            if urlparse(url).path.endswith(image_extension):
                return True
        return False

    @staticmethod
    def _is_url_audio_by_extension(url: str) -> bool:
        """Check if URL is an audio by its extension."""
        audio_extensions = (".mp3",)
        for audio_extension in audio_extensions:
            if urlparse(url).path.endswith(audio_extension):
                return True
        return False

    def resolve_urls(self) -> dict[str, List[URL]]:
        """Public method to return a dictionary of resolved items' URLs."""
        resolved_urls = {"image": [], "audio": [], "other": []}

        for i, sources in self.all_urls.items():
            for source in sources:
                url = source.removesuffix("/")
                if URLResolver._is_url_image_by_extension(url):
                    resolved_urls["image"].append(URL(i, url))
                elif URLResolver._is_url_audio_by_extension(url):
                    resolved_urls["audio"].append(URL(i, url))
                else:
                    resolved_urls["other"].append(URL(i, url))

        if self.check_urls:
            pattern = re.compile(r"\.[a-z]+$")
            undefined_urls = list(
                filter(
                    lambda undefined_url: not re.search(pattern, undefined_url.source),
                    resolved_urls["other"],
                )
            )

            if platform.system() == "Windows":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

            try:
                # extra dependency
                import aiohttp

                async def resolve_urls_images_by_mime_type(urls: List[URL]):
                    """Asynchronously runs tasks, each of which determines whether an URL leads to a picture."""
                    async with aiohttp.ClientSession() as session:
                        tasks = []
                        for url in urls:
                            tasks.append(
                                is_url_image_by_mime_type(session=session, url=url)
                            )
                        await asyncio.gather(*tasks, return_exceptions=True)

                async def is_url_image_by_mime_type(
                    session: aiohttp.ClientSession, url: URL
                ):
                    """Task which modifies final resolved_urls dict by removing an URL from 'other' category and
                    adding it to 'image' if it was resolved as an image by mime type."""
                    image_formats = ("image/png", "image/jpeg", "image/jpg")
                    resp = await session.request("HEAD", url=url.source)
                    if resp.headers["content-type"] in image_formats:
                        resolved_urls["other"].remove(url)
                        resolved_urls["image"].append(url)

                logger.info(
                    f"There are {len(undefined_urls)} urls to resolve. Please, wait..."
                )

                asyncio.run(resolve_urls_images_by_mime_type(undefined_urls))

            except ModuleNotFoundError:
                logger.warning(
                    f"Consider installing extra dependency aiohttp to perform advanced url type resolving. "
                    f"Use: pip install markedrss[aiohttp]"
                )
            except aiohttp.ClientError:
                logger.warning(
                    f"Connection problems. Url type resolving is performed only by its extension."
                )

        return resolved_urls
