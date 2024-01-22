
# **YouTubeChat-App**

Welcome to the YouTube Chatbot, a modern and intuitive application that enhances your video-watching experience! This chatbot allows you to extract valuable insights, engage in meaningful conversations, and explore video content in a whole new way. Below, we've provided a comprehensive guide to help you get started and make the most out of your YouTube experience.

# **Table of Contents** 
- [Usage and Features](#usage-and-features)
- [Other Features](#other-features)
- [Technologies Used](#technologies-used)
- [Contributions](#contributions)
- [Contact Information](#contact-information)
 
# **Usage and Features**
To begin, copy the link of the YouTube video you wish to explore and paste it into the designated input bar within the app. Click the "Analyse Video" button to initiate the process. Once triggered, the app provides a brief summary, displays the video, and presents its transcript—all conveniently accessible within the application.

<br/>  
<img src="https://github.com/AzizBenAli/YouTubeChat-App/assets/116091818/d75ad6d8-d0b9-4768-8469-05eb18aaedf9" alt="Transcript" width="780">
<br/> 
<br/> 
After the video is displayed, you can start asking queries about the video. An important feature is the capability to retrieve the source of the chatbot's answer, highlighted in the video transcript. This enables users to gain more in-depth knowledge about the video content.
<br/>  
<br/> 
<img src="https://github.com/AzizBenAli/YouTubeChat-App/assets/116091818/51a18e00-9c62-466c-96ed-3238d2a868c0" alt="start asking" width="900">
<br/>  
<br/> 
The chatbot is designed to maintain coherent conversations with users, ensuring a dynamic and engaging interaction.
<br/> 
<br/>
<img src="https://github.com/AzizBenAli/YouTubeChat-App/assets/116091818/cf1f3474-f8dd-4b8f-a736-b608c1afcd8e" alt="conversation" width="600">
<br/> 
<br/> 
To reset the app for exploring another video, simply press "Reset All."

# **Implementation Details**

### A Transcript Extractror 
The YouTube API was employed to access and retrieve the transcript of the video.

### A RAG Pipeline [Paper](https://arxiv.org/pdf/2005.11401.pdf)
- Source Retrieval and Summarization: The system retrieves the most relevant information from the transcript relative to the query using advanced RAG technique: Parent Document Retriever.   
- Citing Sources: A notable feature implemented is the citation of sources by the bot. This allows users to assess the veracity of the provided answer, enhancing transparency.      
- Pipeline with Open-Source Models: The pipeline utilizes open-source embeddings from Hugging Face and the Mistral open-source model for processing the retrieval and generation steps.    
### Memory
The conversation module of the chatbot seamlessly incorporates the buffer memory functionality inherent in the Langchain library. 
# **Other Features**
The app is continually under development, with new features in the pipeline. The focus is on enhancing the chatbot's ability to extract relevant information from videos, providing users with an even more comprehensive experience.

# **Technologies Used**

- Mixtral 8×7B: Used for answering queries based on the video transcript.  
- Hugging Face Transformers and Embeddings: Crucial components for various NLP tasks, contributing to the AI's intelligence and understanding.  
- Python: Employed for backend logic due to its versatility, extensive libraries, and robust functionality.  
- Streamlit: Utilized to create the user-friendly interface, ensuring an interactive and seamless user experience.  
- Langchain: Used for developing prompts and agents, enriching the AI Assistant's functionality and adaptability.

# **Commands**
Running the app locally from this repository
clone this repository
Create a new Python environment provided with pip
run pip install -r requirements.txt
run streamlit run chatbot.py
Now open the 'External URL' in your browser. Enjoy the bot.
<br>
<br>
<img width="404" alt="streamlit_app" src="C:\Users\benal\Desktop\streamlit_app.png">
<br>
<br>
" alt="conversation" width="600">
# **Contributions**
Contributions to enhance features or add new capabilities are welcome! Fork the repository, make your changes, and submit a pull request.

# **Contact Information**
For inquiries or feedback, reach out to [benaliazizaba000@gmail.com] 
