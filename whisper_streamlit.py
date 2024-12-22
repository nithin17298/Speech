import streamlit as st
from st_audiorec import st_audiorec
import json
import requests

API_TOKEN=st.secrets["HF_API"]  

st.title("Speech to Sentiment app")
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


API_URL_SA = "https://api-inference.huggingface.co/models/siebert/sentiment-roberta-large-english"



def get_sentiment_from_return(json):
    for each in json[0]:
        if each["label"]=="NEGATIVE":
            negative=each["score"]
        elif each["label"]=="POSITIVE":
            positive=each["score"]
    
    return round(positive,3),round(negative,3)
    round(sentiment[0][0]['score'],3)
wav_audio_data = st_audiorec()
st.subheader("Transcribed text")
if wav_audio_data is not None:
    with st.status("Transcribing...") as status:
        response = requests.post(API_URL, headers=headers, data=wav_audio_data)
        response=response.json()
        status.update(label="Done Transcribing!", state="complete", expanded=False)

    # st.write(response.json()["text"])
    if response is not None:
        st.write(response["text"])
        output_for_sa = {"inputs": response['text']}
        # st.write(output_for_sa)
        sentiment = requests.post(API_URL_SA, headers=headers, json=output_for_sa)
        sentiment=sentiment.json()
        try:
            positive_score,negative_score=get_sentiment_from_return(sentiment)
            return_value=True
        except:
            return_value=False
    st.subheader("Sentiment")
    if sentiment is not None:
        # st.write("Sentiment Positive Score : {sentiment}")
        # st.write(sentiment)
        if return_value==False:
            st.write("No sentiment detected")
        else:
            st.write("Positive Sentiment Score :blush: :" + str(positive_score))
            st.write("Negative Sentiment Score :unamused: :" + str(negative_score))

# st.write(wav_audio_data)
# if wav_audio_data is not None:
#     st.audio(wav_audio_data, format='audio/wav')
    # output = query(wav_audio_data)

    # st.write(wav_audio_data)