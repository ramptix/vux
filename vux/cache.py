from typing import Any, Dict, Optional

import uvicorn


class CACHE:
    """Lazy cache."""
    pages: Dict[str, Any] = {}
    server: Optional[uvicorn.Server] = None
