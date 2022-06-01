
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Request, Query, Form
from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select
from .models import File, FileBase, FileCreate, FileRead, FileUpdate
from app.database.database import get_session
from ...auth.auth import get_current_active_user
from app.services import storage_file
from app.services.file import change_files_url
from pathlib import Path


file_router = APIRouter()


# ---------------
# Create Post
# ---------------
# Тут форм дату надо ставить
@file_router.post("/files/")
def create_file_my(*, 
        session: Session = Depends(get_session), # Полюбому передается -
        # значит надо вынести в отдельный модуль
        # file: File,
        # file_path: UploadFile = File(...),
        file: UploadFile = File(),
        file_type: str = Form(...),
        post_id: int = Form(...),
        
        # current_value: ValueBase = Depends(get_current_active_user)
    ):
    
    # Пытаемся записать файл на диск
    try: 
        full_file_path = storage_file.save_file(
            f'/posts/{post_id}/files', # Путь к директории
            str(Path(file.filename).stem),# Имя файла
            file # Файл для записи
            )
    except:
        raise HTTPException(status_code=404, detail="File not saved")
    dbfile = File(
        file_path = full_file_path,
        file_type = file_type,
        post_id = post_id,
        )
    session.add(dbfile)
    session.commit()
    session.refresh(dbfile)
    print(dbfile)
    return 'db_file' # На выходе убедимся что id это число с помощью пайдантик UserRead


# ---------------
# Read One Value
# ---------------
@file_router.get("/files/{file_id}", response_model=FileRead)
def read_file(*, 
        session: Session = Depends(get_session), 
        file_id: int,
        request: Request,
        # current_user: User = Depends(get_current_active_user)
    ):
    file = session.get(File, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="file not found")
    print(type(file.dict()))
    return file


# ---------------
# Read All Files
# ---------------
@file_router.get("/files/", response_model=List[FileRead])
def read_files(*,
        session: Session = Depends(get_session),
        offset: int = 0, limit: int = Query(default=100, lte=100),
        request: Request,
        post: Optional[str] = Query(None), 
        # current_user: User = Depends(get_current_active_user)
    ):
    print(f'post = {post}')
    query = select(File)
    if post: # Filtring by post
        print("Фильтруем по посту")
        query = query.where(File.post_id == post)
    query = query.offset(offset).limit(limit) # Полюбому включаем
    files = session.exec(query).all()
    files_data = change_files_url(request, files) 
    return files_data
      

# ---------------
# Update Value
# ---------------
@file_router.patch("/files/{file_id}"
    # , response_model=fileUpdate
    )
def update_file(*, # Будут вызываться как kwargs (Даже если не имеют значения по умолчанию)
        session: Session = Depends(get_session), 
        file_id: int, 
        file: FileUpdate,
        # ... - обязательное поле
    ):
    # Если придет пароль то надо его будет - захешировать
    print("Обновление переменной")     
    print(file)    
    db_file = session.get(File, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="User not found")
    print(f"Успешно получили пользователя {type(db_file)}")
    # exclude_unset - не включать значения None чтобы не затереть их в базе
    # это фишка пайдантика
    file_data = file.dict(exclude_unset=True) 

    print(f"Преобразовали в dict {type(file_data)}")
    for key, file in file_data.items():
        print(f"Обрабатываем {key} {file}")
        # более менее эквивалентно db_file.key = file 
        setattr(db_file, key, file) # Обновление в базе данных
    session.add(db_file)
    session.commit()
    session.refresh(db_file)
    return db_file


# ---------------
# Delete File
# ---------------
@file_router.delete("/files/{file_id}")
def delete_file(*, session: Session = Depends(get_session), file_id: int):
    file = session.get(File, file_id)
    # print(file.post_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    storage_file.delete_file(file) # Удаляем аватарку
    session.delete(file) # Удаляем переменную из базы данных
    session.commit()
    return {"ok": True}


