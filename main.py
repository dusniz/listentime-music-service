import os
import sqlite3
import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

music_directory = "/home/nnmore/Documents/test/music/"
songs = os.listdir(music_directory)


async def save_music(music_name: str):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Tracks (name) VALUES (?)', (music_name,))

    connection.commit()
    connection.close()


async def get_music_filename(music_id: str):
    connection = sqlite3.connect("music.db")
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM Tracks WHERE id = ?', (music_id))
    results = cursor.fetchall()

    connection.close()

    for row in results:
        print(row[0])
        return row[0]


@app.get("/music/{music_id}")
async def get_music_by_id(music_id: str):
    return FileResponse(music_directory + str(await get_music_filename(music_id)))


@app.post("/music")
async def post_music(file: UploadFile):
    async with aiofiles.open(os.path.join(music_directory, str(file.filename)), 'wb') as track:
        content = await file.read()
        await track.write(content)
    await save_music(str(file.filename))
    return {"file_name": file.filename}
