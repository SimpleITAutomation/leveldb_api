import os

import plyvel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BaseConfig

DATA_DIR = os.getenv('LOCAL_DATA_DIR', '/tmp/db')

app = FastAPI(
    title='LevelDB Single Server API',
    description='Simple HTTP Layer for LevelDB',
    version='0.1',
    debug=True
)

level_db_client = plyvel.DB(DATA_DIR, create_if_missing=True)


class BasicModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True


class KVPair(BasicModel):
    key: str
    value: str


class BasicModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True


@app.get("/kv/{key}", response_model=KVPair)
async def get_key_value_pair(*, key: str):
    """ Retrieve one key/value pair """

    value = level_db_client.get(bytes(key, encoding='utf-8'))

    if not value:
        raise HTTPException(status_code=404, detail="Key not found")

    return {
        'key': key,
        'value': value
    }


@app.delete("/kv/{key}")
async def delete_key_value_pair(*, key: str):
    """ Delete a key/value pair """

    level_db_client.delete(bytes(key, encoding='utf-8'))

    return {}


@app.post("/kv", response_model=KVPair)
async def set_key_value_pair(*, kv_in: KVPair):
    """ Set a new key/value pair """

    level_db_client.put(bytes(kv_in.key, encoding='utf-8'), bytes(kv_in.value, encoding='utf-8'))

    return {
        'key': kv_in.key,
        'value': kv_in.value
    }
