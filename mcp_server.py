from pydantic import Field
from mcp.server.fastmcp import FastMCP

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
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
