import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.EmployeeApi import router as employees_router
from app.api.RequestApi import router as requests_router
from app.api.SupplierApi import router as suppliers_router
from app.api.RequestSuggestionApi import router as suggestions_router
from app.api.TruckTypeApi import router as truck_types_router
from app.api.SpeedTypeApi import router as speed_types_router
from app.database import init_db

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.include_router(employees_router, prefix="/api", tags=["employees"])
app.include_router(requests_router, prefix="/api", tags=["requests"])
app.include_router(suppliers_router, prefix="/api", tags=["suppliers"])
app.include_router(suggestions_router, prefix="/api", tags=["suggestions"])
app.include_router(truck_types_router, prefix="/api", tags=["truck_types"])
app.include_router(speed_types_router, prefix="/api", tags=["speed_types"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred", "details": str(exc)},
    )