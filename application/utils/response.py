def success_response(data=None, message="Success", code=200, pagination=None):
    response = {
        "code": code,
        "message": message,
        "data": data if data is not None else []
    }

    if pagination:
        response["pagination"] = pagination

    return response

def error_response(message="Error", code=400, data=None):
    return {
        "code": code,
        "message": message,
        "data": data if data is not None else []
    }