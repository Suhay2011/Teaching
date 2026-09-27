import streamlit as st
from openai import OpenAI

API_KEY="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"

client=OpenAI(api_key=API_KEY,base_url="https://api.groq.com/openai/v1")

Model = "openai/gpt-oss-20b"
def generate(prompt):
  try:
    response = client.chat.completions.create(
        model=Model,
        messages=[
         {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content

  except Exception as e:
    return "Error: "+ str(e)

st.set_page_config(page_title="AI Learning assistant ", layout="centered")
st.title("AI Teaching Assistant")
st.write("ask me any thing about your various subjects.")
if "History" not in st.session_state:
  st.session_state.history=[]
question=st.text_input("enter your question: ")
if st.button("ask"):
  if question.strip():
    with st.spinner("Generate response"):
      answer=generate(question)
    st.session_state.history.insert(0,{"question": question, "answer":answer})

  else:
    st.warning("Please enter a question: ")

if st.session_state.history:
  st.markdown("### Conversation History")
  downloaded_text=" "
  for i, chat in enumerate(st.session_state.history,1):
    downloaded_text +=f"Question{i}:\n"
    downloaded_text +=chat["question"]+"\n\n"
    downloaded_text +="Answer:\n"
    downloaded_text +=chat["answer"]+"\n"
    downloaded_text +="\n"+"-"*50+"\n\n"

    st.markdown(
      f"""<div style="
      border:1px solid #ddd;
      border-radius:10px;
      padding:15px;
      margin-bottom:15px;">
      <h4> Question {i}</h4>
      <p><b>{chat["question"]}</b></p>
      <h4> Answer</h4>
      <p>{chat["answer"]}</p>
      </div>
    """,
    unsafe_allow_html=True)

  st.download_button(
    label="Download Conversation",
    data= downloaded_text,
    file_name="conversation.txt",
    mime="text/plain"
)
  st.write("")

  if st.button("clear conversation"):
    st.session_state.history=[]
    st.rerun()