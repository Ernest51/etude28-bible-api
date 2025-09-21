import os
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def load_target():
    target = os.getenv("FASTAPI_TARGET", "server:app")
    for cand in [target, "main:app", "api:app", "app:app"]:
        try:
            mod, attr = cand.split(":")
            if mod == "asgi":
                continue
            m = importlib.import_module(mod)
            return getattr(m, attr)
        except Exception:
            continue
    f = FastAPI(title="Fallback API - 28 rubriques")
    @f.get("/health")
    def _h(): return {"status": "ok", "source": "fallback"}
    return f

app = load_target()

origins = [
    os.getenv("FRONTEND_ORIGIN", "https://etude8-bible.vercel.app"),
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    @app.get("/health")
    def _health():
        return {"status": "ok"}
except Exception:
    pass
