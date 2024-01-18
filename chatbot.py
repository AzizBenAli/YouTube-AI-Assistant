import streamlit as st
import os
from langchain.llms import HuggingFaceHub
import time
from audio_to_text import transcribe_video_to_text
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from text_to_chunks import transcribed_text_to_chunks
from langchain.vectorstores import faiss
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from pytube import YouTube
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.llms import AI21
import pytube
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory,ConversationSummaryBufferMemory
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.document_loaders import TextLoader, DirectoryLoader
def generate_welcoming_message():
    markdown = """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
    }
    .container {
        text-align: center;
        animation: fadeInUp 1s ease-out;
    }
    .title {
        color: #EC5331;

        font-size: 36px;
        margin-bottom: 20px;
    }
    .bot-icon {
        font-size: 72px;
    }
    .description {
        color: #555;
        font-size: 18px;
        line-height: 1.5;
    }
    @keyframes fadeInUp {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    <div class="container">
        <div>
            <h1 class="title">👋 Welcome to Ted, your YouTube ChatBot!</h1>
            <p class="description">Please enter a YouTube video link above and start chatting with Ted!</p>
        </div>
    </div>
    """
    return markdown





def get_vectorstore(chunks):
    try:
     embed=HuggingFaceEmbeddings(encode_kwargs = {'normalize_embeddings': True})
     vectorstore=FAISS.from_documents(chunks,embed)
     return vectorstore
    except Exception as e:
       st.sidebar.error("please enter a valid link and let's chat again ", icon="🚨")

def get_conversation(vectorstore):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3, "k": 4}),
                                           return_source_documents=True,
                                           verbose=True
                                           )
    return qa_chain
def get_conversation_chain(vectorstore):
  memory = ConversationSummaryBufferMemory(
    llm=llm,
    output_key='answer',
    memory_key='chat_history',
    return_messages=True)

  retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.3,"k": 4, "include_metadata": True})

  chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    get_chat_history=lambda h : h,
    verbose=False)
  return chain


def get_conversation_chain_advanced(vectorstore):
  loader = DirectoryLoader(r"C:\Users\benal\Langchain\Youtube",
                             glob='*.txt',
                             loader_cls=TextLoader)

  documents = loader.load()
  memory = ConversationSummaryBufferMemory(
    llm=llm,
    output_key='answer',
    memory_key='chat_history',
    return_messages=True)
  bm25_retriever = BM25Retriever.from_documents(documents)
  bm25_retriever.k =3
  chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
  ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5])
  chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    chain_type="stuff",
    retriever= ensemble_retriever,
    return_source_documents=True,
    get_chat_history=lambda h : h,
    verbose=False)
  return chain
 
def get_video_chara(url):
   try:
    yt = YouTube(url)
    video_title = yt.title
    video_duration = yt.length
    video_thumbnail = yt.thumbnail_url
    return  video_title,video_duration,video_thumbnail
   except pytube.exceptions.RegexMatchError:
        return None, None, None

def type_effect(response, source_highlighted):
    if response:
        words = response.split()
        displayed_text = st.empty()
        highlighted_text = st.empty()
        for i in range(len(words)):
            displayed_text.write(" ".join(words[:i+1]))
            time.sleep(0.2)
            if i == len(words) - 1:
                highlighted_text.markdown(source_highlighted, unsafe_allow_html=True)
                break

summaries_cache = {}
def get_summary(video_key, documents):
    if video_key not in summaries_cache:
        prompt_template = """Write a concise summary of the following "{text}"
                            CONCISE SUMMARY:"""
        prompt = PromptTemplate.from_template(prompt_template)
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
        summary = stuff_chain.run(documents)
        summaries_cache[video_key] = summary
    return summaries_cache[video_key]

def find_and_highlight_sentence(paragraph, target_sentence, transcribed_text):
        if target_sentence in transcribed_text:
            highlighted_sentence = f"<span style=' color: red;'>{target_sentence}</span>"
            return paragraph.replace(target_sentence, highlighted_sentence)
        return paragraph
    
os.environ['HUGGINGFACEHUB_API_TOKEN']=''
llm1= HuggingFaceHub(repo_id='mistralai/Mixtral-8x7B-Instruct-v0.1', model_kwargs={'temperature': 0.1, 'max_length': 64},verbose=True)
llm = AI21(ai21_api_key='',temperature=0.1,verbose=False)

if 'conversation' not in st.session_state:
    st.session_state.conversation=None
if 'empty_space' not in st.session_state:
    st.session_state.empty_space = st.empty() 
    welcoming_message = generate_welcoming_message()
    st.session_state.empty_space.markdown(welcoming_message, unsafe_allow_html=True)
if 'num' not in st.session_state:
    st.session_state.num=None


st.sidebar.markdown(
    f"<h1 style='color: #EC5331; font-size: 36px; font-weight: bold;'>YouChat App</h1>", 
    unsafe_allow_html=True
)
st.sidebar.title('▶️ Provide a YouTube Video Link')
url = st.sidebar.text_input("Paste the YouTube Video Link here", value="", help="E.g., https://www.youtube.com/watch?v=your_video_id")
if url!="":
    st.session_state.num=True
col1, col2 = st.sidebar.columns(2)
with col1:
  ask_button = st.button("Analyze Video 🚀")
with col2:
  reset_button = st.button("Reset Form 🔄")
if reset_button:
    directory = r'C:\Users\benal\Langchain\Youtube'
    for filename in os.listdir(directory):
     file_path = os.path.join(directory, filename)
     if os.path.isfile(file_path):
        os.remove(file_path)
    url=""
    st.session_state.messages = []
    ask_button=True
    if  st.session_state.num:
     st.sidebar.info("please enter a new video link and let's chat again",icon="ℹ️")
    st.session_state.conversation=None
    st.session_state.documents=None
if 'documents' not in st.session_state:
  st.session_state.documents = None
if 'chunks' not in st.session_state:
  st.session_state.chunks = None
if 'vectorstore' not in st.session_state:
  st.session_state.vectorstore = None
if 'transcribed_text' not in st.session_state:
  st.session_state.transcribed_text = None

if url!="" :
    if ask_button:
        with st.sidebar:
         st.session_state.messages = []
         st.session_state.conversation=None
         with st.spinner("Analyzing the Video... 🕵️‍♂️"):
          ask_button=False
          st.session_state.transcribed_text= transcribe_video_to_text(url)
          st.session_state.documents,st.session_state.chunks=transcribed_text_to_chunks(r'c:\Users\benal\Langchain\Youtube')
          st.session_state.vectorstore=get_vectorstore(st.session_state.chunks)
          if st.session_state.vectorstore is not None:
           st.session_state.conversation=get_conversation_chain_advanced( st.session_state.vectorstore)

if url!="" :
    with st.sidebar:
     video_title, video_duration, video_thumbnail = get_video_chara(url)
     if video_title is not None and video_duration is not None and video_thumbnail is not None and st.session_state.documents is not None :
      summary = get_summary(url,st.session_state.documents)
      video_id=id=url.split("=")[-1]
      st.markdown("<h1 style='color: #EC5331;'>📽️ Video Details</h1>", unsafe_allow_html=True)
      st.markdown(f"<p style='font-size: 18px;'><strong><span style='color:#EC5331;'>Summary:<br></span></strong> {summary}</p>", unsafe_allow_html=True)
      st.markdown(f'<iframe width="490" height="315" src="https://www.youtube.com/embed/{video_id}?start={90}&autoplay=1" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
      transcript=st.markdown(f"<div style='height: 400px; overflow-y: scroll;'>{st.session_state.transcribed_text}</div>", unsafe_allow_html=True)


if 'messages' not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'],unsafe_allow_html=True)
if st.session_state.conversation is not None :
  prompt = st.chat_input('Message to ChatBot...')
  if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role':'user','content': prompt})
    response= f'Echo {prompt}'
    response=st.session_state.conversation(prompt)
    with st.spinner("Thinking...Please  wait..."):
        time.sleep(1)
    with st.chat_message('assistant'):
        answer=response.get("answer")
        doc=response['source_documents']
        if doc:
           source = str(doc[0]).split("\\")[-1].replace(".txt'}", "")
           answer_final = f"{answer} \n\n Source: {video_title} Video"
           transcribed_text_highlited=st.session_state.transcribed_text
           for i in range(len(doc)):
            transcribed_text_highlited = find_and_highlight_sentence(transcribed_text_highlited, doc[i].page_content,st.session_state.transcribed_text)
           transcript.markdown(f"<div style='height: 400px; overflow-y: scroll;'>{transcribed_text_highlited}</div>", unsafe_allow_html=True)  
        else:
           source = 'your AI assistant'
           answer_final = f"{answer} \n\n Source: {source}"
        segments = answer_final.split("\n\n")
        segments[-1] = f"<span style='color: #EC5331;'>{segments[-1]}</span>"
        answer_final=f"{segments[0]} \n\n {segments[-1]}"
        st.markdown(answer_final,unsafe_allow_html=True)
        st.session_state.messages.append({'role':'assistant','content':answer_final})



