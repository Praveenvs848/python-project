from fastapi import FastAPI ,Request,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse,JSONResponse
import time
import json
from agent import graph
import pdfplumber

import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
from langchain_core.messages import AIMessageChunk, HumanMessage

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
extracted_texts = {}

@app.get("/")
async def index():
    return "hello world is now working"

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Get file details
    file_name = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Extract text from the PDF
    extracted_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text()  # Extract text from et from the page
                extracted_texts["text"]=extracted_text
            print(extracted_text)
    except Exception as e:
        return JSONResponse(content={"error": f"Error extracting text: {str(e)}"}, status_code=500)
    
    return JSONResponse(content={"message": f"File {file_name} uploaded successfully!", "text": extracted_text})
# Streaming endpoint
@app.post("/stream")
async def stream(request: Request):
    # Parse the JSON body
    body = await request.json()
    print(body)
    query=body["query"]
    dataa=extracted_texts["text"]
    async def event_stream():
        prompt = f"""
    You are an AI assistant. Use the following Uploaded File data to answer the user's question:

    User's Question: {query}

    Uploaded File Data:
    {dataa}
    
    
    
    Provide the answer in Markdown format, including appropriate headings, lists, or other Markdown elements as necessary.
    
    """
        

        inputs = [HumanMessage(content=query)]
        first = True
        gathered = None  # Initialize a variable to accumulate chunks of AI message

        # Start streaming the responses
        async for event in graph.astream_events({"messages": prompt}, version="v1"):
            kind = event["event"]
            
            print(f"{kind}: {event['name']}")
            # print(event)

            if kind=="on_chat_model_stream" :
                agent = event["metadata"]["langgraph_node"]
                if agent=="answer_agent":
                    data=event["data"]["chunk"].content
                    jdata={"agent":"answer_agent","text":data}
                    dump=json.dumps(jdata)

                    yield f"{dump}\n"
                if agent=="usermessage_agent":
                    data=event["data"]["chunk"].content
                    jdata={"agent":"usermessage_agent","text":data}
                    dump=json.dumps(jdata)

                    yield f"{dump}\n"
            
            else:
                pass
            
            

    return StreamingResponse(event_stream(), media_type="text/event-stream")
