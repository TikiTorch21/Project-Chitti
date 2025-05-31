This goal of this project is to build a RAG tool using Streamlit that allows users to upload documents and interact with them using a 'chatbot'. This project will take advantage of LLM's to retrieve relevant information from uploaded documents and general coversational responses.

<u><b>How it works:</b></u>
1. Uses Streamlit to create a UI for the user to upload a pdf
2. Ask the chatbot a question related to the pdf uploaded
3. Watch as the LLM pulls text from the uploaded pdf to answer the user query!
	- Also adds citations

<u>What does the Streamlit UI include specifically?</u>
	So far, it includes a:
	<pre>
	- File upload section
	- Chat window
	- Export answer
	</pre>

What are some <u>non-functional features?</u>
1. Peformance
	- Quick resolution of user queries and support for documents up to 10 MB.
2. Portability
	- Package the tool as a local application runnable on any system. 
3. Documentation
	- Provide comprehensive user and technical documentation. 
	- User guide: Steps to upload documents and interact with the tool.
	- Developer guide: Setup, codebase architecture, etc. 


## TO DO:
### For the webapp
- Preview height - has to be longer
- change the ‘show pymupdf text’ to something like ‘show extracted text’, etc- something cleaner.
- Don’t make the default scroll down, because there is nothing in the chat - making you scroll for no reason
- Improve the default text preset from "Type your message here..." to something else (maybe ‘Ask Chitti’ would be ideal)
- Add a mock LLM response to the question asked by just repeating the question. (Just to repsresent a placeholder for the actual LLM response)
- Remove the “Ask Chitti” header(makes window look disorganized)
- Fix the "clear chat" button alignment under the chat window.
    - brainstorm how do you want to show citations (ideally under the chat windows)
- PDF Name: {pdf-name} on the left sidebar before preview, Update the current

### Documentation
- Finish PDF report