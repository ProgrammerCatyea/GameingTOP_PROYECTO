import os
from io import BytesIO
from uuid import uuid4
from typing import Optional

from fastapi import UploadFile, HTTPException
from supabase import create_client, Client

from backend.core.config import settings


def get_supabase_client() -> Client:
    if not settings.supabase_url or not settings.supabase_service_role_key:
        raise RuntimeError(
            "Supabase no está configurado. "
            "Verifica SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY en el .env"
        )

    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def generate_image_path(
    filename: Optional[str],
    folder: str = "rankings",
) -> str:
    if not filename:
        filename = "image.jpg"

    _, ext = os.path.splitext(filename)
    if not ext:
        ext = ".jpg"

    unique_name = f"{uuid4().hex}{ext}"
    return f"{folder}/{unique_name}"


async def upload_image_to_supabase(
    file: UploadFile,
    path: Optional[str] = None,
    folder: str = "rankings",
) -> str:

    supabase = get_supabase_client()
    bucket_name = settings.supabase_bucket_name or "rankings-images"


    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")


    if not path:
        path = generate_image_path(file.filename, folder=folder)

    resp = supabase.storage.from_(bucket_name).upload(
        path,
        BytesIO(content),
    )


    if isinstance(resp, dict) and resp.get("error"):
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo subir la imagen a Supabase: {resp['error']}",
        )

  
    public_url = supabase.storage.from_(bucket_name).get_public_url(path)

    return public_url


def delete_image_from_supabase(path: str) -> None:
    """
    Elimina un archivo del bucket de Supabase dado su path interno.
    """
    supabase = get_supabase_client()
    bucket_name = settings.supabase_bucket_name or "rankings-images"

 
    resp = supabase.storage.from_(bucket_name).remove([path])

    if isinstance(resp, dict) and resp.get("error"):
       
        print("Error al eliminar imagen de Supabase:", resp["error"])
