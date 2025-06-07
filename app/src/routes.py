# External imports
from typing import Optional
import traceback
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

# Internal imports
from app.src.orchestrators.registry import PROCESSOR_REGISTRY

router = APIRouter()

class ProcessRequest(BaseModel):
    job_type: str
    file_name: Optional[str]
    file_content: Optional[str]
    extraction_schema: Optional[list[dict]]


@router.post("/process")
async def process_document(request: ProcessRequest):

    # Obtain job type
    job_type = request.job_type

    if not job_type or job_type not in PROCESSOR_REGISTRY:
        raise HTTPException(status_code=400, detail="Invalid job type")

    # Assign the processor
    processor = PROCESSOR_REGISTRY[job_type]()

    # Remove 'file_type' and pass the rest to .run()
    run_args = {k: v for k, v in request.dict().items() if k != "job_type"}

    try:
        result = processor.run(**run_args)
        return {"status": "success", "result": result}
    except Exception as e:
        traceback.print_exc()  # This prints full traceback in your console
        raise HTTPException(status_code=500, detail=str(e))
    

