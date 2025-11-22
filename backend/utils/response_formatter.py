from typing import Any, Dict, Optional

def success_response(
    data: Any = None,
    message: str = "Operación exitosa",
    status_code: int = 200,
) -> Dict[str, Any]:
  
    return {
        "status": "success",
        "status_code": status_code,
        "message": message,
        "data": data,
    }


def error_response(
    message: str = "Ocurrió un error inesperado",
    status_code: int = 400,
    details: Optional[str] = None,
) -> Dict[str, Any]:
   
    return {
        "status": "error",
        "status_code": status_code,
        "message": message,
        "details": details,
    }
