# """
# FastAPI application entry point
# """
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from app.config.settings import settings
# from app.schemas import AgentRequest, AgentResponse
# from app.agents import create_agent_graph
# from app.utils import setup_logging
# from app.agents.master_agent import run_agent
# import logging
# import asyncio

# # Setup logging
# setup_logging()
# logger = logging.getLogger(__name__)

# # Create FastAPI app
# app = FastAPI(
#     title=settings.app_name,
#     version=settings.app_version,
#     debug=settings.debug,
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.on_event("startup")
# async def startup_event():
#     """On application startup"""
#     logger.info(f"Starting {settings.app_name} v{settings.app_version}")
#     logger.info(f"LLM Provider: {settings.llm_provider}, Model: {settings.model_name}")


# @app.on_event("shutdown")
# async def shutdown_event():
#     """On application shutdown"""
#     logger.info(f"Shutting down {settings.app_name}")


# @app.get("/")
# async def root():
#     """Root endpoint"""
#     return {
#         "app": settings.app_name,
#         "version": settings.app_version,
#         "status": "running",
#     }


# @app.get("/health")
# async def health():
#     """Health check endpoint"""
#     return {"status": "healthy"}


# @app.post("/agent/chat", response_model=AgentResponse)
# async def agent_chat(request: AgentRequest) -> AgentResponse:
#     """
#     Chat with the agent
    
#     Args:
#         request: Agent request with query and optional history
        
#     Returns:
#         Agent response
#     """
#     try:
#         if not request.query:
#             raise HTTPException(status_code=400, detail="Query cannot be empty")
        
#         logger.info(f"Processing query: {request.query[:100]}...")
        
#         # Run agent
#         result = await run_agent(
#             query=request.query,
#             conversation_history=request.conversation_history,
#         )
        
#         return AgentResponse(
#             response=result.get("response", ""),
#             reasoning=None,
#             tools_used=None,
#             metadata=request.metadata,
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error in agent chat: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# @app.post("/agent/stream")
# async def agent_stream(request: AgentRequest):
#     """
#     Stream responses from the agent (for interactive chat)
    
#     Args:
#         request: Agent request
        
#     Yields:
#         Streaming response chunks
#     """
#     async def generate():
#         try:
#             result = await run_agent(
#                 query=request.query,
#                 conversation_history=request.conversation_history,
#             )
#             yield f"data: {result.get('response', '')}\n\n"
#         except Exception as e:
#             logger.error(f"Error in agent stream: {str(e)}")
#             yield f"data: Error: {str(e)}\n\n"
    
#     return generate()


# if __name__ == "__main__":
#     import uvicorn
    
#     uvicorn.run(
#         "main:app",
#         host=settings.host,
#         port=settings.port,
#         reload=settings.debug,
#     )
