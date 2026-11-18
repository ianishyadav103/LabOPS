from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure packages directory exists to prevent startup crash
if os.path.exists("packages"):
    app.mount("/packages", StaticFiles(directory="packages"), name="packages")

connected_agents = {}
dashboard_ws = None

@app.get("/")
async def get_dashboard():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws/dashboard")
async def dashboard_endpoint(websocket: WebSocket):
    global dashboard_ws
    await websocket.accept()
    dashboard_ws = websocket
    print("[+] Master Dashboard Connected")
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        dashboard_ws = None
        print("[-] Master Dashboard Disconnected")

@app.websocket("/ws/agent/{agent_id}")
async def agent_endpoint(websocket: WebSocket, agent_id: str):
    await websocket.accept()
    connected_agents[agent_id] = websocket
    print(f"[+] Agent {agent_id} Connected")
    try:
        while True:
            data = await websocket.receive_json()
            if dashboard_ws:
                await dashboard_ws.send_json(data)
    except WebSocketDisconnect:
        if agent_id in connected_agents:
            del connected_agents[agent_id]
        print(f"[-] Agent {agent_id} Disconnected")

# Dynamic Instruction Gateway Endpoint
@app.post("/api/dispatch")
async def dispatch_instruction(request: Request):
    payload = await request.json()
    target_agent_id = payload.get("target_agent_id")  # Check if a specific target was selected
    
    if target_agent_id and target_agent_id != "ALL":
        # Send only to the selected targeted system
        if target_agent_id in connected_agents:
            await connected_agents[target_agent_id].send_json(payload)
            return {"status": f"Instruction sent to {target_agent_id}", "agents": 1}
        else:
            return {"status": f"Agent {target_agent_id} not found", "agents": 0}
    else:
        # Broadcast to all connected systems
        for agent_id, ws in connected_agents.items():
            await ws.send_json(payload)
        return {"status": "Instruction Dispatched to All", "agents": len(connected_agents)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)