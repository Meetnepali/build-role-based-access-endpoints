# Guidance for Task

This project provides a FastAPI-based backend for user profile management, including asynchronous secure upload and storage of profile profile pictures. 

Your primary goal is to implement endpoints that allow users to:
- Create a new user profile (with username, email, bio—profile picture optional).
- Retrieve a user profile by username (including picture URL if set).
- Upload/update a profile picture for an existing user (enforcing secure checks: only PNG/JPEG images up to 1MB, file saved asynchronously and filename stored in-memory). 

All user data and file references must be kept in-memory (no persistent database).

You should:
- Properly structure routes using FastAPI routers.
- Use Pydantic models to define and validate request and response schemas.
- Validate uploaded images for content type and size.
- Save uploaded images into a local `media/` directory.
- Return clear and structured JSON error responses for invalid input (bad file type, too large, missing user, etc.).
- Use only the provided requirements and keep the code concise and organized.
- Containerize the application using Docker as provided in the codebase.

## Verifying Your Solution

Make sure:
- Your API endpoints adhere to the described behavior, return correct HTTP status codes and use structured error responses.
- Uploaded files are validated, saved, and referenced properly in-memory as specified.
- The solution uses routers, at least two code files, and the specified Python/Docker setup.
- The OpenAPI docs are populated with endpoint information and tags.

You can verify your solution is complete by checking that each of these requirements is met and the application behavior matches the description above.
