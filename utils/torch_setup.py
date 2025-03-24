import os
import torch
import asyncio

def setup_torch():
    """Setup torch and asyncio environment"""
    # Disable CUDA if not available
    if not torch.cuda.is_available():
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # Setup event loop policy
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        # For non-Windows systems
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    
    # Create new event loop if needed
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)