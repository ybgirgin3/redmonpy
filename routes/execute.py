from fastapi import APIRouter, Request, status


from commons.models import Command


router = APIRouter(prefix="/execute", tags=["execute"])


@router.get("/", response_description="run command", response_model=None)
async def execute(req: Request, command: Command):
    # TODO: run command here
    pass
