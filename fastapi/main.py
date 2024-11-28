from fastapi import FastAPI, HTTPException
import redis.asyncio as redis
app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.redis = redis.Redis(host="redis", port=6379)

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()

@app.post("/send-task/")
async def send_task(query: str):
    redis_client = app.state.redis
    message_id = await redis_client.xadd("queue_a", {"query": query})
    return {"status": "Task added", "message_id": message_id}