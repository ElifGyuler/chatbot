import json

# .ipynb dosyasından bağlamı almak için fonksiyon
def get_context_from_ipynb(filename: str) -> str:
    # Dosyayı açma ve JSON olarak okuma
    with open(filename, 'r') as f:
        notebook_data = json.load(f)  # .ipynb dosyasını JSON formatında okur

    # Notebook'taki hücrelerdeki (cell) metni çekme
    context = ""
    for cell in notebook_data['cells']:
        if cell['cell_type'] == 'code':
            # Eğer bir kod hücresi ise, içeriğini alıyoruz
            context += "\n".join(cell['source'])  # Kod hücresindeki metni alıyoruz
        elif cell['cell_type'] == 'markdown':
            # Eğer bir markdown hücresi ise, içeriğini alıyoruz
            context += "\n".join(cell['source'])  # Markdown hücresindeki metni alıyoruz
    return context

# Fonksiyonu kullanmak için
context = get_context_from_ipynb('context.ipynb')  # .ipynb dosyasını buraya geçirin

import streamlit as st
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser  # Structured parser


context = get_context_from_ipynb('context.ipynb')

# Wrap the prompt in a function
def prompt_fn(query: str, context: str) -> str:
    return f"You are a knowledgeable learning assistant. Your users are asking questions about the article and other things related to the article. Answer the user's question using only the given context. If you don't know the answer, you should make further research and try to give a logical answer. Use up to ten sentences and be concise in your response.\n\nContext: {context}\n\nUser's question: {query}"

# Wrap the prompt function in a RunnableLambda
prompt_runnable = RunnableLambda(lambda inputs: prompt_fn(inputs["query"], inputs["context"]))

# LLM (ChatOpenAI model)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)

# Define the chain using the wrapped prompt and the LLM
rag_chain = prompt_runnable | llm

# Streamlit UI
def run_chatbot():
    # Sidebar
    st.sidebar.title("Discover Me")
    st.sidebar.image("IMG_1551.jpg", caption="Elif Gyuler")  # Replace with your image file
    st.sidebar.write(
        """
        Hi, I'm Elif, got Master's degree from Groningen University, semi-professional photographer an AI enthusiast. I created this chatbot to assist you 
        with answering questions about Master's thesis and related to various articles/topics of it. Feel free to ask me anything!
        """
    )
    st.sidebar.title("The Effect of Fear on Election Results: Rally-Round-The-Flag-Effect and The Case of Turkey")
    st.sidebar.write("""
        The two most chaotic periods in Turkey's electoral history are June 7-November 1, 2015, and
April 16, 2017. The main reason for this is that both elections were held under the shadow and
fear of terrorism. Therefore, the Turkish people prioritized avoiding terrorism and ending the
atmosphere of fear in both chaotic periods. In the international relations literature, a
phenomenon directly examines the relationship between crisis environments and elections in
depth: the rally-round-the-flag effect. This phenomenon, created by Mueller, investigated and
linked the extent to which voters' decisions change in crises. After Mueller, scholars have
examined this phenomenon under the headings of 'patriotism' and 'opinion leadership.' In the
research based on this phenomenon, the differences in votes before and after terrorist acts, field
studies conducted by research firms, and the content of speeches made by political leaders were
analyzed. As a result, based on the scope of the terrorist acts, the conclusion reached is that the
Turkish people acted with the effect of 'patriotism' during the June 7-November 1 period,
leading to a 9% increase in the AKP's vote. The April 16, 2017 referendum, on the other hand,
led to a more chaotic outcome as the scope of the FETO coup attempt directly threatened the
entire country and the symbols of the Turkish people (TBMM, TSK) and both 'patriotism' and
'opinion leadership' effects were observed. Finally, the rally-round-the-flag effect refers to a
critical concept still debated: "the diversionary use of force." This debate about political figures
creating/expanding chaos for political gains is an area that still needs to be deepened. In the
case of Turkey, however, in both electoral processes, Erdoğan's AKP made political gains by
fighting against 'imaginary enemies' based on real threats. In this sense, this debate is an area
that needs to be deepened in Turkey.
    """)

    # Main page
    st.markdown("""
    <h1 style="display: inline; vertical-align: middle;">AI Assistant MARS</h1>
""", unsafe_allow_html=True)
    st.write("""
        Welcome to my AI-powered chatbot! Feel free to ask questions about any article or topic you're curious about. 
        I will answer as concisely and accurately as possible based on the given context. 
        Let's get started!
    """)

    # Article Context Section
    
    query = st.text_input("Ask a Question")

    # If the user submits a query
    if st.button("Get Answer"):
        if context and query:
            inputs = {"query": query, "context": context}
            response = rag_chain.invoke(inputs)
            st.write("Response:", response)
        else:
            st.warning("Please provide a question.")
    st.markdown("Response")

if __name__ == "__main__":
    run_chatbot()

