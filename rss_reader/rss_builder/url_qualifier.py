import asyncio
import logging
import platform
import re
from urllib.parse import urlparse

logger = logging.getLogger("rss-reader")


class URLQualifier:
    def __init__(self, urls, check_urls):
        self.all_urls = urls
        self.check_urls = check_urls

    @staticmethod
    def _is_url_image_by_extension(url: str):
        image_extensions = (".png", ".jpeg", ".jpg")
        for image_extension in image_extensions:
            if urlparse(url).path.endswith(image_extension):
                return True
        return False

    @staticmethod
    def _is_url_audio_by_extension(url: str):
        audio_extensions = (".mp3",)
        for audio_extension in audio_extensions:
            if urlparse(url).path.endswith(audio_extension):
                return True
        return False

    def determine_urls(self):
        results = {"image": [], "audio": [], "other": []}
        for i, urls in self.all_urls.items():
            for url in urls:
                url = url.removesuffix("/")
                if URLQualifier._is_url_image_by_extension(url):
                    results["image"].append((i, url))
                if URLQualifier._is_url_audio_by_extension(url):
                    results["audio"].append((i, url))
                else:
                    results["other"].append((i, url))

        if self.check_urls:

            async def is_url_image_by_mime_type(session, url, results):
                image_formats = ("image/png", "image/jpeg", "image/jpg")
                resp = await session.request("HEAD", url=url[1])
                if resp.headers["content-type"] in image_formats:
                    results["other"].remove(url)
                    results["image"].append(url)

            async def determine_urls_images_by_mime_type(urls, results):
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for url in urls:
                        tasks.append(
                            is_url_image_by_mime_type(
                                session=session, url=url, results=results
                            )
                        )
                    await asyncio.gather(*tasks, return_exceptions=True)

            pattern = re.compile(r"\.[a-z]+$")
            undefined_urls = list(
                filter(
                    lambda undefined_url: not re.search(pattern, undefined_url[1]),
                    results["other"],
                )
            )

            if platform.system() == "Windows":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

            try:
                import aiohttp

                logger.info(f"There are {len(undefined_urls)} urls to check!")

                asyncio.run(determine_urls_images_by_mime_type(undefined_urls, results))
            except ModuleNotFoundError:
                logger.warning(
                    f"Consider installing extra dependency aiohttp to perform advanced url type resolving. "
                    f"Use: pip install markedrss[aiohttp]"
                )
            except aiohttp.ClientError:
                logger.warning(
                    f"Connection problems. Url type resolving is performed only by its extension."
                )

        return results
