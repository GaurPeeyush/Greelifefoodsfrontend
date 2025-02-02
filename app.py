import streamlit as st
import requests
import json
from datetime import datetime

# Updated API URL
API_URL = "https://justapi-bay.vercel.app/"
#http://localhost:8000/chat

def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_time' not in st.session_state:
        st.session_state.current_time = datetime.now().strftime("%H:%M")

def chat_with_bot(query: str):
    """Send chat request to deployed API and return response"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30  # Added timeout for API requests
        )
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()["response"]
    except requests.exceptions.Timeout:
        return "Error: The request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the server. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        return f"Error: The server returned an error. Status code: {e.response.status_code}"
    except Exception as e:
        return f"Error: Unable to get response from server. {str(e)}"

def clear_chat_history():
    """Clear both local and server chat history"""
    try:
        # Clear server-side history
        requests.post(
            f"{API_URL}/chat",
            json={"query": "", "clear_history": True},
            headers={"Content-Type": "application/json"}
        )
        # Clear client-side history
        st.session_state.messages = []
    except Exception as e:
        st.error(f"Error clearing chat history: {str(e)}")

def main():
    st.set_page_config(
        page_title="GreenLife Foods Assistant",
        page_icon="🌱",
        layout="wide"
    )

    # Initialize session state
    init_session_state()

    # Custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: #d1d8bd;
        }
        
        /* Header styling */
        .header {
            background: #283106;
            padding: 2rem 1rem;
            border-radius: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }
        
        .header h1 {
            color: white !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        /* Chat container */
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 1.5rem;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        /* Message bubbles */
        .user-message {
            background: #2e7d32;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 20px 20px 4px 20px;
            margin: 1rem 0;
            max-width: 70%;
            margin-left: auto;
            position: relative;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .bot-message {
            background: #f3faf4;
            color: #283106;
            padding: 1rem 1.5rem;
            border-radius: 20px 20px 20px 4px;
            margin: 1rem 0;
            max-width: 70%;
            position: relative;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .message-time {
            font-size: 0.75rem;
            color: #888;
            margin-top: 0.5rem;
            display: block;
        }
        
        /* Avatar styling */
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            position: absolute;
            bottom: -10px;
        }
        
        .user-avatar {
            right: -45px;
            background: #2e7d32 url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24px" height="24px"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>') center/60% no-repeat;
        }
        
        .bot-avatar {
            left: -45px;
            background: #66bb6a url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24px" height="24px"><path d="M0 0h24v24H0z" fill="none"/><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>') center/60% no-repeat;
        }
        
        /* Input area */
        .stTextInput input {
            border: 2px solid #e0e0e0 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
        }
        
        .stTextInput input:focus {
            border-color: #66bb6a !important;
            box-shadow: 0 0 0 3px rgba(102,187,106,0.2) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #e0e0e0;
            padding: 1rem;
        }
        
        .sidebar-section {
            margin: 2rem 0;
        }
        
        .sidebar-section h3 {
            color: #2e7d32;
            font-weight: 600;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 0.5rem;
        }
        
        /* Button styling */
        .stButton button {
            background: #2e7d32 !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(46,125,50,0.2);
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            color: #666;
            padding: 2rem 0;
            margin-top: 3rem;
            font-size: 0.9rem;
        }
            /* Target the <input> element within the text input widget */
    [data-testid="stTextInput"] input {
        background-color: #283106 !important;
    }
        </style>
    """, unsafe_allow_html=True)

    # Page header
    st.markdown("""
        <div class="header">
            <div style="max-width: 800px; margin: 0 auto;">
                <div style="display: flex; align-items: center; gap: 1rem; justify-content: center;">
                    <h1>GreenLife Product Assistant</h1>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-section">
                <h3>About Us</h3>
                <p style="color: #555; line-height: 1.5;">Discover nature's finest organic products, sustainably sourced and delivered with care.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="sidebar-section">
                <h3>Quick Links</h3>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <a href="#" style="color: #2e7d32; text-decoration: none; padding: 8px 12px; border-radius: 8px; transition: all 0.2s;">📦 Product Catalog</a>
                    <a href="#" style="color: #2e7d32; text-decoration: none; padding: 8px 12px; border-radius: 8px; transition: all 0.2s;">📜 Certification Info</a>
                    <a href="#" style="color: #2e7d32; text-decoration: none; padding: 8px 12px; border-radius: 8px; transition: all 0.2s;">🕒 Order History</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧹 Clear Chat History", type="secondary"):
            clear_chat_history()

    # Main chat container
    # st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; color: #283106;">
            <h2>Hey there! My name is Greenie! 🌿</h2><br>
            <h6 style = "color: #2e7d32">I'm here to help streamline the order capture process for GreenLife Foods! 🥦🍎</h6>
            <h6 style = "color: #2e7d32">Whether you're a distributor or a retailer, I can assist you with placing orders, checking availability, and answering any questions about our organic food products.</h6>
            <h6 style = "color: #2e7d32">Let's make ordering simple and efficient! 🚀</h6>
        </div>
    """, unsafe_allow_html=True)


    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div style="position: relative;">
                    <div class="user-message">
                        {message["content"]}
                        <span class="message-time">{message["time"]}</span>
                    </div>
                    <div class="avatar user-avatar"></div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="position: relative;">
                    <div class="bot-message">
                        {message["content"]}
                        <span class="message-time">{message["time"]}</span>
                    </div>
                    <div class="avatar bot-avatar"></div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input
    with st.container():
        col1, col2, col3 = st.columns([1,6,1])
        with col2:
            user_input = st.text_input(
                "Ask about our organic products...",
                key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
            
            if st.button("Send Message", key="send_button"):
                if user_input.strip():
                    # Add user message to chat
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_input,
                        "time": datetime.now().strftime("%H:%M")
                    })

                    # Get bot response
                    bot_response = chat_with_bot(user_input)

                    # Add bot response to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response,
                        "time": datetime.now().strftime("%H:%M")
                    })

                    # Clear input
                    st.rerun()

    # Footer
    st.markdown("""
        <div class="footer">
            <p>🌱 Committed to Sustainable Nutrition • support@greenlifefoods.com • © 2024 GreenLife Foods</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
