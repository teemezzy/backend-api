from app.schemas import GenericResponse
from typing import Any, Optional

class ResponseContentFormatter:
    def __init__(self):
        self.response_code_to_message = {
            0: "Success",
            1: "Generic Error",
            2: "Not Live",
            3: "Not Registered",
            4: "Not Verified",
            5: "Not Authorized",
            6: "Not Found",
            7: "Is Live",
        }
    
    def get_response_by_code(
            self,
            reponse_code: int,
            details: dict = {},
            user=None
        ) -> GenericResponse:
        return GenericResponse(
            message=self.response_code_to_message[reponse_code],
            error_code=0,
            details=details,
            user=user
        ).__dict__


response_content_formatter = ResponseContentFormatter()
