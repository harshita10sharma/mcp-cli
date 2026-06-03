from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts  import base 
mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
        name = "read_doc",
        description="USe this tool to read the content written inside a document"
)
def read_document(
    doc_id: str=Field(description="provide the id of document")
):
    if doc_id not in docs:
        raise ValueError(f"Document having {doc_id} not found")
    return docs[doc_id]
# TODO: Write a tool to edit a doc
@mcp.tool(
        name = "edit_doc",
        description="use this tool to replace the old string in a document with the new string."
)
def edit_doc(
    doc_id: str = Field(description="Id of the document in which u wanna edit"),
    old_str: str = Field(description="Enter the old string you want to edit"),
    new_str: str = Field(description="Enter the new string")
):
    if doc_id not in docs:
        raise ValueError
    docs[doc_id] =  docs[doc_id].replace(old_str,new_str)


#TODO: Write a resource to return all doc's ids
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())
# TODO: Write a resource to return the contents of a particular doc
    
@mcp.resource(
    "docs://document/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document having {doc_id} not found")
    return docs[doc_id]
# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name = "format",
    description = "Rewrites the contents of the doc into MarkDown format"
)
def format_document(
    doc_id : str = Field(description = "Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>{doc_id}</document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'read_doc' tool to read the document, then use the 'edit_doc' tool to edit it.
    """
    return [base.UserMessage(prompt)]
@mcp.prompt(
    name="summary",
    description="Summarizes the contents of a document"
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize")
) -> list[base.Message]:
    prompt = f"""
    Your goal is to summarize a document clearly and concisely.

    The id of the document you need to summarize is:
    <document_id>{doc_id}</document_id>

    Read the document content, then provide a brief summary with the key points.
    """
    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
