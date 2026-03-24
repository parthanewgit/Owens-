#!/usr/bin/env python
"""Start the FastAPI backend server."""

import uvicorn
import sys

if __name__ == "__main__":
    print("Starting FastAPI backend server...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
