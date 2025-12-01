from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success(data=None, message="success"):
    if data is None:
        data = {}
    else:
        # convert ORM models or complex objects to JSON-compatible
        data = jsonable_encoder(data)
    return JSONResponse(
        content={
            "data": data,
            "status": {"code": "200", "message": message}
        }
    )
def not_found(message="Not found"):
    return JSONResponse(
        content={
            "data": {},
            "status": {"code": "400", "message": message}
        }
    )

def internal_error(message="Internal server error"):
    return JSONResponse(
        content={
            "data": {},
            "status": {"code": "500", "message": message}
        }
    )