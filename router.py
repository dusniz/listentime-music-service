from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
import sqlite3
import os
import aiofiles

router = APIRouter(
        prefix="/music",
        )

music_directory = "./music/"

class Music:
    name: str
    def __init__(self, name):
        self.name = name


async def save_music(music: Music):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Tracks (name) VALUES (?)', (music.name,))

    connection.commit()
    connection.close()


async def get_music_filename(music_id: str):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM Tracks WHERE id = ?', (music_id))
    results = cursor.fetchall()

    connection.close()

    return results[0][0]


@router.get("/{music_id}")
async def get_music_by_id(music_id: str):
    return FileResponse(music_directory + str(await get_music_filename(music_id)))


@router.post("")
async def post_music(file: UploadFile):
    async with aiofiles.open(os.path.join(music_directory, str(file.filename)), 'wb') as track:
        content = await file.read()
        await track.write(content)
    await save_music(Music(str(file.filename)))
    return {"file_name": file.filename}
