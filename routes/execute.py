from fastapi import APIRouter, Request
import dacite


from commons.models import Command
from orm import RedOrm


router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("/", response_description="run command", response_model=None)
async def execute(req: Request, cmd: dict):
    # TODO: run command here
    print("command", cmd)
    # command = dacite.from_dict(Command, cmd)
    command = Command(**cmd)
    print(command)
    red = RedOrm()
    return {
        "response": red.execute(
            command.command, command.key, command.val, command.force  # type: ignore
        )
    }
