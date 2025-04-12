from flask import jsonify

class ApiResponse:

    @staticmethod
    def ok(data=None, total=None, page=None, per_page=None):
        """
        200 OK - General successful GET response.
        """
        response_data = {
            "success": True,
            "result": {
                "total": total if total is not None else len(data) if data else 0,
                "items": data if data else [],
                "page": page,
                "per_page": per_page
            },
            "status": 200
        }
        return jsonify(response_data), 200
    
    @staticmethod
    def ok_single(data=None):
        """
        200 OK - Successful GET response for a single element.
        """
        response_data = {
            "success": True,
            "result": data,
            "status": 200
        }
        return jsonify(response_data), 200

    @staticmethod
    def created(data=None):
        """
        201 CREATED - Response for resource creation.
        """
        response_data = {
            "success": True,
            "result": {
                "items": data if data else []
            },
            "status": 201,
            "message": "Resource created successfully."
        }
        return jsonify(response_data), 201

    @staticmethod
    def updated(data=None, updated_fields=None):
        """
        200 OK - Response for resource update.
        """
        response_data = {
            "success": True,
            "result": {
                "items": data if data else [],
                "updated_fields": updated_fields if updated_fields else []
            },
            "status": 200,
            "message": "Resource updated successfully."
        }
        return jsonify(response_data), 200

    @staticmethod
    def deleted(deleted_id):
        """
        200 OK - Response for resource deletion.
        """
        response_data = {
            "success": True,
            "result": {
                "items": [
                    {
                        "deleted_id": deleted_id
                    }
                ]
            },
            "status": 200,
            "message": "Resource deleted successfully."
        }
        return jsonify(response_data), 200

    @staticmethod
    def bad_request(missing_field=None, message=None):
        """
        400 BAD REQUEST - Response for invalid request.
        """
        response_data = {
            "success": False,
            "result": {
                "details": {
                    "missing_field": missing_field,
                    "message": message
                }
            },
            "status": 400,
            "message": "Invalid request parameters."
        }
        return jsonify(response_data), 400

    @staticmethod
    def not_found(resource, resource_id=None):
        """
        404 NOT FOUND - Response for missing resource.
        """
        if resource_id is None:
            response_data = {
                "success": False,
                "result": {
                    "details": {
                        "resource": resource,
                        "message": f"No {resource} available or no results match the criteria."
                    }
                },
                "status": 404,
                "message": f"No {resource} found."
            }
        else:
            response_data = {
                "success": False,
                "result": {
                    "details": {
                        "resource": resource,
                        "id": resource_id,
                        "message": f"{resource} with id {resource_id} does not exist."
                    }
                },
                "status": 404,
                "message": "Resource not found."
            }
        return jsonify(response_data), 404

    @staticmethod
    def conflict(field=None, value=None, message=None):
        """
        409 CONFLICT - Response for conflict in the request.
        """
        response_data = {
            "success": False,
            "result": {
                "details": {
                    "field": field,
                    "value": value,
                    "message": message
                }
            },
            "status": 409,
            "message": f"Conflict: {message}"
        }
        return jsonify(response_data), 409

    @staticmethod
    def internal_server_error():
        """
        500 INTERNAL SERVER ERROR - Response for unexpected server errors.
        """
        response_data = {
            "success": False,
            "result": None,
            "status": 500,
            "message": "An internal server error occurred. Please try again later."
        }
        return jsonify(response_data), 500
