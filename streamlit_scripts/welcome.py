import streamlit as st

def welcome():
    st.title("🏠🎾 Welcome to the Tennis Stats Dashboard")
    st.markdown("""
    This app helps you explore proffessional tennis matches from 2020 to 2024.      
    """)

    col1, col2 = st.columns(2)
    col1.image("https://tse2.mm.bing.net/th/id/OIP.uyG6pVYYYjmc4BhgzszYWAAAAA?rs=1&pid=ImgDetMain&o=7&rm=3",)
    col2.image("https://tse1.mm.bing.net/th/id/OIP.8TK135JtIvN-7vKjyIBfFQHaEK?rs=1&pid=ImgDetMain&o=7&rm=3",)

    st.header("""
                Ready to dive into the world of tennis analytics?  
    """)

    st.markdown("""    
    Use the tabs above to navigate through the features.  
    """)

    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            color: #6c757d;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        </style>
        <div class="footer">
            Made using Streamlit | © 2025 Am-Egej<br>  
            The data will be updated on the 31st of December every year. 
                The next update will be on 31/12/2025.
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    welcome()