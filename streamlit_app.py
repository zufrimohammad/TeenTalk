# Import required libraries
from dotenv import load_dotenv
from itertools import zip_longest

import streamlit as st
from streamlit_chat import message
import time

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


# Load environment variables
load_dotenv()

# Set streamlit page configuration
api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Platform Curhatmu")
st.title("TeenTalk : Platform Curhat Terbaikmu")

# Initialize session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []  # Store AI generated responses

if "past" not in st.session_state:
    st.session_state["past"] = []  # Store past user inputs

if "entered_prompt" not in st.session_state:
    st.session_state["entered_prompt"] = ""  # Store the latest user input


# Initialize the ChatOpenAI model
chat = ChatOpenAI(temperature=0.5, model_name="gpt-4o")

def build_message_list():
    """
    Build a list of messages including system, human and AI messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [
        SystemMessage(
            content="The Professional Guidance and Counseling Assistants, who are available to guide students in personal, social, academic, and career matters. If the question is outside the area of counseling guidance or the areas mentioned above, please respond with 'That is beyond my ability' or 'I cannot answer that'.If you would like to 'report', 'bullying', 'chat', 'personal matters', 'family problems', 'direct consultation', 'consultation'. You may contact your Guidance Counselor based on your class."
        )
    ]

    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(
        st.session_state["past"], st.session_state["generated"]
    ):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Create a text input for user
st.text_input("Tuliskan Curhatanmu disini... ", key="prompt_input", on_change=submit)


# Buat fungsi untuk menampilkan progress bar dengan durasi yang disesuaikan
def display_progress_bar(duration):
    progress_text = "Kami sedang memproses curhatmu..."
    progress_text_placeholder = st.empty()  # <-- Ini harus ada
    progress_text_placeholder.write(progress_text)  # <-- Dan ini juga
    my_bar = st.progress(0)

    increment = 0.01  # Setiap increment ini akan menambah progress bar sebesar 1%
    num_updates = int(duration // increment)

    for idx in range(num_updates):
        time.sleep(increment)
        current_progress = (
            idx + 1
        ) / num_updates  # Menghitung progress berdasarkan iterasi saat ini
        my_bar.progress(current_progress)

    # Pastikan progress bar mencapai 100% di akhir durasi
    my_bar.progress(1)
    time.sleep(0.5)
    my_bar.empty()
    progress_text_placeholder.empty()


# Get user query and check for trigger words within the same block
if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Mulai penghitungan waktu
    start_time = time.time()

    # Generate response
    output = generate_response()

    # Hitung durasi yang diperlukan untuk menghasilkan respons
    elapsed_time = time.time() - start_time

    # Tampilkan progress bar dengan durasi yang telah diukur
    display_progress_bar(elapsed_time)

    # Append AI response to generated responses
    st.session_state.generated.append(output)

    # Check for specific user keywords to trigger the report functionality
    trigger_words = [
        "laporkan",
        "pembulian",
        "ingin chat",
        "pribadi",
        "masalah keluarga",
        "konsultasi langsung",
        "konsultasi",
    ]
    if any(word in user_query.lower() for word in trigger_words):
        report_message = "Permisi ibu, saya ingin ..."  # pesan awal yang akan muncul di chat WhatsApp

        st.write(
            """
                Anda Juga dapat Menghubungi **:orange[Guru Bimbingan Konseling]** Secara Langsung dengan Menekan Tombol yang ada di Bawah ini
            """
        )

        st.link_button(
            "Klik Tombol ini untuk Kelas 7 (Bu May)",
            f"https://api.whatsapp.com/send?phone=6285294603683&text={report_message}",
        )
        st.link_button(
            "Klik Tombol ini untuk Kelas 8 (Bu Larisa)",
            f"https://api.whatsapp.com/send?phone=6287834913339&text={report_message}",
        )
        st.link_button(
            "Klik Tombol ini untuk Kelas 9 (Bu Silia)",
            f"https://api.whatsapp.com/send?phone=6285759217336&text={report_message}",
        )

# Display the chat history
if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")


# Add credit
st.markdown(
    """
---
 Mari Bicara, Mari Tumbuh"""
)

# Sidebar
st.sidebar.title("TeenTalk")
st.sidebar.subheader("Platform Curhat Terbaikmu")
st.sidebar.markdown(
    """
**TeenTalk** dirancang untuk membantu siswa dengan pertanyaan-pertanyaan mengenai **bimbingan konseling**. 
Untuk menggunakannya, cukup ketikkan pertanyaan atau pernyataan Anda pada kotak chat dan Anda akan mendapatkan tanggapan dari ChatBot.
"""
)
with st.sidebar.expander("Butuh Bantuan Langsung?"):
    st.write(
        """
        Jika Anda menghadapi masalah serius seperti **:blue[pembulian]** atau memerlukan **:blue[bantuan langsung dari guru BK]**, 
Anda dapat menyampaikannya langsung melalui platform ini. **:blue[Ketik pesan Anda]** dan robot akan mengarahkan Anda 
untuk berkomunikasi langsung dengan guru BK melalui WhatsApp atau dapat menekan tombol dibawah ini berdasarkan kelasnya
    """
    )
    report_message = "Permisi ibu, saya ingin ..."
    st.link_button(
        "Menghubungi Guru BK Kelas 7 (Bu May)",
        f"https://api.whatsapp.com/send?phone=6285294603683&text={report_message}",
    )
    st.link_button(
        "Menghubungi Guru BK Kelas 8 (Bu Larisa)",
        f"https://api.whatsapp.com/send?phone=6287834913339&text={report_message}",
    )
    st.link_button(
        "Menghubungi Guru BK Kelas 9 (Bu Silia)",
        f"https://api.whatsapp.com/send?phone=6285759217336&text={report_message}",
    )
