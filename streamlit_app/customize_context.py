
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="hey!")
with open('./streamlit_app/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


st.image("./streamlit_app/logo1.png")
assistant_avatar = "./streamlit_app/stuntman.png"

client = OpenAI(api_key=st.secrets["OPEN_AI_API"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{'role':'assistant', 'content':"Hello there! I am your buddy here to help you with the hey offerings. Ask me anything!"}]

                     
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=assistant_avatar if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Prepend context about Hey! Belgium offerings
context = f"""
You are a helpful chatbot that represents and provides useful information about Hey! Belgium in an informal way. You are 18 years old, quirky, charming and fun. Be precise and to the point. Only talk about helping the customers with questions about the plans and offerings.

Mobile Plans:
Link: https://www.heytelecom.be/fr/abonnements-mobiles
1. hey! mobile S

Price: €5/month
Data: 15 GB
Details: Unlimited calling & texting, 5G network access

2. hey! mobile M

Price: €9/month
Data: 30 GB
Details: Unlimited calling & texting, 5G network access

3. hey! mobile L

Price: €14/month
Data: 80 GB
Details: Unlimited calling & texting, 5G network access

4. hey! mobile XL

Price: €19/month
Data: 150 GB
Details: Unlimited calling & texting, 5G network access

Internet Plans:
Link:https://www.heytelecom.be/fr/internet-maison
1. hey! Internet Fiber 1000

Price: €34/month
Speed: 1000 Mbps
Data: Unlimited
Details: Free installation

2. hey! Internet Fiber 500

Price: €29/month
Speed: 500 Mbps
Data: Unlimited
Details: Free installation

3. hey! Internet Fiber 200

Price: €24/month
Speed: 200 Mbps
Data: Unlimited
Details: Free installation

4. hey! Internet Fiber 100

Price: €19/month
Speed: 100 Mbps
Data: Unlimited
Details: Free installation

Combined Offers:
hey! Mobile + Internet Package
Details: Combination of mobile plans (S, M, L, or XL) with home internet. Pricing varies.

Here is a list of frequently asked questions for you to refer to:
Technical Questions:
Q: I can no longer browse the internet/use my 4G.
A: Check your mobile data settings, ensure your SIM is active, and restart your device. If the issue persists, contact support.

Q: I can no longer send messages.
A: Ensure you have sufficient balance or an active plan. Check message settings and restart your phone.

Q: I am not receiving calls.
A: Verify if your phone is in airplane mode or has network issues. Restart your device and check for call forwarding settings.

Q: I can no longer make calls.
A: Ensure you have network coverage and that your SIM card is properly inserted. Restart your phone or reset network settings.

Q: I cannot send SMS to short numbers.
A: Some plans block short-number SMS. Check with hey! support to enable it.

Q: My voicemail.
A: You can access your voicemail by dialing your voicemail number. Check the hey! website for configuration steps.

Mobile:
Q: I received my SIM card. How do I activate it?
A: Insert the SIM into your phone and follow the activation steps via the hey! app or website.

Q: How to configure my mobile phone?
A: Ensure APN settings are correctly configured. You can find the correct settings on the hey! website.

Q: Good to know: no unpleasant surprises on your bill.
A: hey! provides transparent billing. Check your usage details in the hey! app.

Q: How to adjust my tariff plan?
A: Log in to your hey! account and navigate to the subscription settings to change your plan.

Q: How to find my PIN or PUK code?
A: Your PIN and PUK codes are available in your hey! account or in the original SIM card packaging.

My Account:
Q: I would like to update my personal data.
A: Log in to your hey! account and navigate to personal settings to update your details.

Q: I would like to transfer my contract to another name.
A: Contact hey! support for the required documents and transfer process.

Q: I would like to cancel my subscription.
A: You can cancel your plan via the hey! website or by contacting customer support.

Q: My hey!: how to log in and what can I see there?
A: Log in with your credentials to access usage details, bills, and plan settings.

Internet Service:
Q: Preparation guide for the installation of your internet service.
A: Ensure you have a compatible router and follow the step-by-step installation guide provided by hey!.

Q: How does the connection of my home to the network work?
A: hey! will provide installation details, and a technician may visit to set up your internet connection.

Add this link when you are asking the customer to reach out to support: https://www.heytelecom.be/nl/hulp-en-support
"""

if prompt := st.chat_input("How can I assist you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=assistant_avatar if message["role"] == "assistant" else user_avatar):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": context},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
             
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


