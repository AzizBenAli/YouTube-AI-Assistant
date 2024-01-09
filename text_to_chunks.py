from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def transcribed_text_to_chunks(url):
 loader = DirectoryLoader(url,
                             glob='*.txt',
                             loader_cls=TextLoader)

 documents = loader.load()
 text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=60,
 )
 chunks=text_splitter.split_documents(documents)
 return documents,chunks
