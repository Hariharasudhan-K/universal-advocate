import streamlit as st
import time
import os
from universal_advocate.agents import IntakeAgent, ResearcherAgent, VerifierAgent, WriterAgent

# Page Config
st.set_page_config(page_title="Universal Advocate", page_icon="🛡️", layout="wide")

# Title & Banner
st.title("🛡️ Universal Advocate: AI Dispute Resolver")
st.markdown("""
**Agents Intensive Capstone Project** | *Track: Agents for Good*
> "Automating consumer justice through multi-agent AI."
""")

# Sidebar: Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
if not api_key:
    # Try to load from env
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        st.sidebar.success("API Key loaded from environment")
    else:
        st.sidebar.warning("Please enter your API Key to proceed.")

# Main Interface
st.header("Start Your Case")

with st.form("intake_form"):
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("Your Name", "John Doe")
        user_email = st.text_input("Email", "john@example.com")
        user_address = st.text_area("Address", "123 Main St, City, State")
    with col2:
        company = st.text_input("Company Name", "Delta Airlines")
        amount = st.text_input("Dispute Amount ($)", "500")
        purchase_date = st.date_input("Purchase Date")
    
    issue_description = st.text_area("Describe your issue in detail", height=150, 
                                     placeholder="e.g., My flight was delayed by 5 hours and they refused to refund me...")
    
    submitted = st.form_submit_button("Generate Legal Strategy")

if submitted and api_key:
    # Initialize Agents
    try:
        intake = IntakeAgent(api_key)
        researcher = ResearcherAgent(api_key)
        verifier = VerifierAgent(api_key)
        writer = WriterAgent(api_key)
        
        # Progress Container
        status_container = st.container()
        
        with status_container:
            st.info("🕵️ Intake Agent: Analyzing your case...")
            # In a full app, IntakeAgent would parse the text. Here we use the form data directly 
            # but we could use the agent to extract extra tags.
            analysis = intake.analyze_issue(issue_description)
            st.write(f"**Analysis:** {analysis}")
            time.sleep(1)
            
            st.info("📚 Research Agent: Searching for relevant policies...")
            # Determine sector roughly (or use Intake analysis if parsed correctly)
            sector = "General" 
            policy_data = researcher.find_policy(company, sector, issue_description)
            st.write(f"**Found Policy:** [{policy_data['url']}]({policy_data['url']})")
            st.caption(policy_data['text'])
            time.sleep(1)
            
            st.info("⚖️ Verifier Agent: Checking source credibility...")
            is_authentic = verifier.verify_source(policy_data['url'], company)
            if is_authentic:
                st.success("Source Verified ✅")
            else:
                st.warning("Source Unverified ⚠️ - Proceeding with caution.")
            time.sleep(1)
            
            st.info("📝 Writer Agent: Drafting your legal demand letter...")
            context = {
                "user_name": user_name,
                "user_email": user_email,
                "user_address": user_address,
                "company": company,
                "amount": amount,
                "issue": issue_description,
                "purchase_date": str(purchase_date),
                "ref_number": "N/A", # Could add field
                "payment_method": "Original Payment Method", # Could add field
                "policy_text": policy_data['text'],
                "policy_url": policy_data['url']
            }
            letter = writer.write_letter(context)
            user_reply = writer.write_user_reply(context)
            
        # Results Display
        st.divider()
        st.subheader("✅ Your Action Plan")
        
        tab1, tab2 = st.tabs(["📜 Legal Demand Letter", "💬 Agent Strategy"])
        
        with tab1:
            st.text_area("Copy this letter:", value=letter, height=600)
            st.download_button("Download Letter", letter, file_name="demand_letter.txt")
            
        with tab2:
            st.markdown(user_reply)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

elif submitted and not api_key:
    st.error("Please provide a Google Gemini API Key to run the agents.")
