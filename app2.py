import streamlit as st
import pandas as pd
import pyttsx3
import io
import os

def text_to_speech(text):
    """
    Convert input text to speech using pyttsx3 library
    
    Args:
        text (str): Input text to convert to speech
    
    Returns:
        bytes: Audio file in bytes
    """
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Create an in-memory bytes buffer
    audio_buffer = io.BytesIO()
    
    # Save audio to the buffer
    engine.save_to_file(text, audio_buffer)
    engine.runAndWait()
    
    # Reset buffer position
    audio_buffer.seek(0)
    
    return audio_buffer.getvalue()

def main():
    """
    Main Streamlit application for text-to-speech conversion
    """
    # Set page title and icon
    st.set_page_config(page_title="CSV Text-to-Speech Converter", page_icon="🔊")
    
    # Title and description
    st.title("CSV Text-to-Speech Converter 🎙️")
    st.write("Upload a CSV file and convert text to speech!")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    # Column selection
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display column names
        st.write("Available Columns:", list(df.columns))
        
        # Column selection dropdown
        text_column = st.selectbox("Select the column with text to convert", df.columns)
        
        # Text preview
        st.subheader("Text Preview")
        preview_rows = st.slider("Select number of rows to preview", 1, min(10, len(df)), 3)
        st.dataframe(df[text_column].head(preview_rows))
        
        # Conversion buttons
        if st.button("Convert Selected Column to Speech"):
            try:
                # Combine text from selected column
                full_text = " ".join(df[text_column].dropna().astype(str))
                
                # Convert to speech
                audio_bytes = text_to_speech(full_text)
                
                # Play audio
                st.audio(audio_bytes, format='audio/wav')
                
                # Download button
                st.download_button(
                    label="Download Audio File",
                    data=audio_bytes,
                    file_name="text_to_speech_output.wav",
                    mime="audio/wav"
                )
                
                st.success("Text successfully converted to speech!")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
