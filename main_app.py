
import streamlit as st
from PIL import Image
import json
import requests  
from langchain.callbacks import get_openai_callback  
from backend_api.visualization import Visualization
from backend_api.database import DatabaseConnection
import hmac
import streamlit as st

def check_password():

    def login_form():
        st.set_page_config(page_title="LexoGraph", layout="wide")
        
        logo_url = "/home/ramai.saud/Downloads/images.jpeg"
        st.image(logo_url, width=100)
        
        st.title("LexoGraph")

        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()


def main():
    if "history" not in st.session_state:
        st.session_state.history = []

    st.set_page_config(
        page_title="LexoGraph",
        page_icon=":bar_chart:",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        body {
            background-color: #87CEEB; /* Sky Blue */
            font-family: 'Arial', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    logo_col, title_col = st.columns([1, 3])

    with logo_col:
        image_path = "/home/ramai.saud/Downloads/images.jpeg"
        logo_image = Image.open(image_path)
        st.image(logo_image, caption="LexoGraph", use_column_width=False, width=100)
    
    user_question = st.text_input("Enter your question:")

    history = st.session_state.history
    data_for_visualization = None  
    data_for_visualization_json = None  
    cloudinary_image_url = None 

    with get_openai_callback() as cb:
        if st.button("Generate Visualization") and user_question.strip():
            with st.spinner("Please Wait!"):
                user_question_prompt = f"I dont know my database try to fix the db column names and find me {user_question} and return a string value"
                response = DatabaseConnection.agent_executor.run(input={'query': user_question_prompt}, handle_parsing_errors=True)

                if isinstance(response, (tuple, list)) and len(response) >= 2:
                    _, data_for_visualization_json = response
                else:
                    data_for_visualization_json = response

                if not isinstance(data_for_visualization_json, str):
                    st.error("Unexpected response format. Expected a string.")
                    return

                try:
                    data_for_visualization = json.loads(data_for_visualization_json)
                    st.write("")
                    st.write(data_for_visualization)

                except json.JSONDecodeError:
                    st.write("Output:")
                    st.write(data_for_visualization_json)

                cloudinary_image_url = Visualization.open_interpreter(data_for_visualization_json, cloudinary_folder="lexograph")

                if cloudinary_image_url is not None:
                    st.image(cloudinary_image_url, caption="Generated Visualization", use_column_width=True)
                    st.success("Image uploaded successfully!") 
                    history_item = (user_question, data_for_visualization, cloudinary_image_url)
                    history.append(history_item)    

                    token_info_table = {
                        "Total Tokens": cb.total_tokens,
                        "Prompt Tokens": cb.prompt_tokens,
                        "Completion Tokens": cb.completion_tokens,
                        "Total Cost (USD)": cb.total_cost
                    }
                    st.table(token_info_table)
                    api_payload = {
                        "question": user_question,
                        "data_for_visualization": json.dumps(data_for_visualization),
                        "cloudinary_image_url": cloudinary_image_url
                    }

                    api_url = "http://localhost:8000/ask-question"  
                    response = requests.post(api_url, json=api_payload)

                    if response.status_code == 200:
                        st.success("Visualization details sent to backend.")
                    else:
                        st.error("Failed to send visualization details to backend.")

    st.sidebar.header("Visualization History")
    for idx, (query, data_for_visualization, cloudinary_image_url) in enumerate(history, start=1):
        st.sidebar.markdown(f"**Message {idx}:** {query}")
        st.sidebar.image(cloudinary_image_url, caption=f"Visualization {idx}", use_column_width=True)

if __name__ == "__main__":
    main()
