from imp import reload
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sql import crud, database, models, schemas
from sql.database import db_state_default

database.db.connect()
database.db.create_tables([models.ScaleRecord])
database.db.close()

app = FastAPI()
''' 允许跨域访问 '''
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sleep_time = 3


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


@app.get("/")
def read_root():
    return "Hello World!"


@app.get("/record/{record_id}",
         response_model=schemas.ScaleRecord,
         dependencies=[Depends(get_db)])
def read_record(record_id: int):
    db_record = crud.get_record(record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record


@app.get("/records/{scale_id}",
         response_model=List[schemas.ScaleRecord],
         dependencies=[Depends(get_db)])
def read_records_by_scale_id(scale_id: str):
    records = crud.get_records_by_scaleid(scale_id=scale_id)
    return records


# 这里暂时先不用一个接口通过get和post区分, 因为可能会漏掉
@app.post("/newrecord/",
          response_model=schemas.ScaleRecord,
          dependencies=[Depends(get_db)])
def create_record(record: schemas.ScaleRecordCreate):
    return crud.create_scale_record(record=record)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)