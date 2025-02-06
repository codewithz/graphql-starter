import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Define a GraphQL schema
@strawberry.type
class User:
    id: str
    name: str
    email: str

@strawberry.type
class UpdateUserResponse:
    success: bool
    message: str

# Sample user data
users = {
    "12345": User(id="12345", name="John Doe", email="john.doe@example.com")
}

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: str) -> User:
        return users.get(id, User(id=id, name="Unknown", email="unknown@example.com"))

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user(self, id: str, name: str) -> UpdateUserResponse:
     if id in users:
        users[id] = User(id=id, name=name, email=users[id].email)  # Correct assignment
        return UpdateUserResponse(success=True, message="User updated successfully")
     return UpdateUserResponse(success=False, message="User not found")


# Create a GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# FastAPI app
app = FastAPI()

# GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
