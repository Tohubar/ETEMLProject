import sys

def error_message_details(error, error_details: sys):
    _, _, exc_tb  = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    err_message = f"Error occured in the file {file_name} in the line number {exc_tb.tb_lineno}. Error message -> {error}"
    return err_message

class UsVisaException(Exception):
    def __init__(self, error, error_detail: sys):
        super().__init__(error)

        self.err_msg =  error_message_details(error, error_detail)

    def __str__(self):
        return self.err_msg