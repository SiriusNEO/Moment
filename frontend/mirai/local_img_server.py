from frontend.mirai.frontend_config import IMG_PATH
from graia.application.message.elements.internal import Image

tmp_file_name = "tmp"

async def save_image(data: bytes, file_name=tmp_file_name):
    path = IMG_PATH + file_name
    fp = open(path, "wb")
    fp.write(data)
    fp.close()
    return path

async def download_image(url: str):
    return await Image.http_to_bytes(Image(), url)


