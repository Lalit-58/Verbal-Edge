import streamlit as st
import docx
import fitz
from lang import get_counter_argument
def extract_text(file):
    if file.name.endswith(".pdf"):      
        doc =fitz.open(stream=file.read(), filetype="pdf")
        text=""
        for page in doc:
            text+= page.get_text()
        return text
    elif file.name.endswith('.docx'):
        docx_file = docx.Document(file)
        return "\n".join([para.text for para in docx_file.paragraphs])
    elif file.name.endswith(".txt"):
        return file.read().decode("UTF-8")
    else:
        return ""
st.set_page_config(page_title="VerbalEdge", page_icon=":robot:", layout="centered")
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
st.title("Verbal Edge")
st.markdown(
    """Welcome to verbal Edge, your AI-powered debate assistant! :robot:\n\n
       Pick a topic to start a debate with your AI opponent.

       This bot will simulate by presenting arguments for both sides.
       """)
st.markdown("---")
if "debate_started" not in st.session_state:
    st.session_state.debate_started = False
if "memory_state" not in st.session_state:
    st.session_state.memory_state = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "topic" not in st.session_state:
    st.session_state.topic = None
if "side" not in st.session_state:
    st.session_state.side = None
if "doc_text" not in st.session_state:
    st.session_state.doc_text = None
if "user_current_side" not in st.session_state:  # 🛠️ NEW
    st.session_state.user_current_side = None  

st.subheader("Choose Input Method: ")
input_method = st.radio("Select Input Method", ["Upload a Document", "Enter a Custom topic"], index=0)
topic, doc_text= None, None
st.markdown("---")
#Uploading a document
Uploaded_File = None
if input_method == "Upload a Document":
    st.subheader("Upload a Document:")
    Uploaded_File = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
    if Uploaded_File is not None:
        st.success(f"Uploaded: {Uploaded_File.name}")
        topic= f"Debate based on the uploaded Document: {Uploaded_File.name}"
        doc_text = extract_text(Uploaded_File)


elif input_method == "Enter a Custom topic":
    topic = st.text_input("Enter your Debate topic:",placeholder="E.g. Is Social Media Beneficial or Harmful to society?")
    doc_text = topic if topic else None


st.markdown("---")
st.subheader("Select your position:")
side=st.radio("Select your position",["Pro","Con"],index=0,horizontal= False)
st.subheader("Start the Debate")
start_debate = st.button("Start Debate")

if start_debate:
    if not doc_text:
        st.warning("Please provide a topic or upload a document to start the debate")
    else:
        st.session_state.debate_started = True
        st.session_state.topic = topic
        st.session_state.side = side
        st.session_state.doc_text = doc_text
        st.session_state.chat_history = []
        st.session_state.memory_state = None
        st.session_state.user_current_side = side 
        st.success(f"Debate started on: **{topic}**")
if st.session_state.debate_started:
    if st.button("End Debate"):
        st.session_state.debate_started = False
        st.session_state.chat_history = []
        st.session_state.memory_state = None
        st.success("Debate ended. You can start a new debate now.")
        st.stop()
if st.session_state.debate_started:
    if input_method == "Upload a Document" and not Uploaded_File:
        st.warning("Please upload a Document first.")
    elif input_method == "Enter a Custom topic" and not topic:
        st.warning("Please enter a topic to start the debate.")
    else:
        if Uploaded_File:
            doc_text= extract_text(Uploaded_File)
            st.session_state.doc_text = doc_text
        else:
            st.session_state.doc_text = topic
        st.session_state.topic = topic
        st.session_state.side= side
        st.session_state.debate_started = True

        st.success(f"Debate started on: **{topic}**")
if st.session_state.debate_started:
    # st.success(f"Debate started on:**{st.session_state.topic}**")
    st.chat_message("user").markdown(f"You are arguing: **{st.session_state.side}**")

    for role, message in st.session_state.chat_history:
        
        st.chat_message(role).markdown(message)

    user_input = st.chat_input("Enter your argument here...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        ai_stance = "Con" if st.session_state.user_current_side == "Pro" else "Pro"
        with st.chat_message("AI"):
            with st.spinner("Typing..."):

                ai_response, updated_memory = get_counter_argument(
                    Topic=st.session_state.topic,
                    Stance= ai_stance,
                    User_argument=user_input,
                    doc_text=st.session_state.doc_text,
                    memory=st.session_state.memory_state,
        )
        st.markdown(ai_response)
        st.session_state.memory_state = updated_memory
        st.session_state.chat_history.append(("ai", ai_response))
        #st.session_state.side = ai_stance
        st.chat_message("ai").markdown(ai_response)

        st.rerun()

st.markdown("---")

st.caption(" VerbalEdge UI | Designed with Streamlit")


