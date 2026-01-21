from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.schema import schema


app = FastAPI(
    title="Clarke Energia API",
    description="API GraphQL para simulação de economia de energia",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema, graphiql=True)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {
        "message": "Clarke Energia API",
        "status": "online",
        "graphql": "/graphql"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}