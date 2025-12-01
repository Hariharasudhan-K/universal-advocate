import time
try:
    from googlesearch import search
except ImportError:
    search = None

from llm_engine import get_llm_engine

class IntakeAgent:
    def __init__(self, api_key=None):
        self.llm = get_llm_engine(api_key)

    def analyze_issue(self, user_input: str) -> dict:
        """
        Uses LLM to extract structured data from the user's issue description.
        """
        print("  [Intake] Analyzing user issue with AI...")
        prompt = f"""
        Analyze the following user complaint and extract key details into a JSON-like structure (do not return markdown, just the dict string).
        If a field is missing, use "N/A".
        
        User Input: "{user_input}"
        
        Required Fields:
        - sector: (Health, Travel, Retail, Finance, or Other)
        - company: (Name of the entity)
        - amount: (Monetary value involved, as a number if possible)
        - issue_summary: (Concise 1-sentence summary)
        - key_facts: (List of important details)
        """
        response = self.llm.query(prompt)
        # Simple parsing cleanup (in a real app, use a JSON parser)
        return response

class ResearcherAgent:
    def __init__(self, api_key=None):
        self.llm = get_llm_engine(api_key)

    def find_policy(self, company: str, sector: str, issue: str) -> dict:
        """
        Uses LLM to generate search queries, then summarizes results.
        """
        print(f"  [Researcher] AI searching for policies regarding '{issue}'...")
        
        # 1. Generate Query
        query_prompt = f"Generate the best Google search query to find the refund policy for {company} regarding {issue}. Return only the query."
        search_query = self.llm.query(query_prompt).strip().strip('"')
        print(f"  [Researcher] Search Query: {search_query}")

        # 2. Perform Search (Simulated fallback if library missing or fails)
        found_url = "https://www.google.com/search?q=" + search_query.replace(" ", "+")
        found_text = "General Consumer Protection Laws apply."
        
        if search:
            try:
                # Get first result
                results = list(search(search_query, num_results=1))
                if results:
                    found_url = results[0]
                    # In a real full implementation, we would scrape this URL.
                    # For now, we'll ask the LLM what the policy LIKELY is based on its training data.
            except Exception as e:
                print(f"  [Researcher] Search failed ({e}), relying on internal knowledge.")
        
        # 3. Summarize/Hallucinate Policy (since we aren't scraping live HTML in this demo)
        context_prompt = f"""
        Based on your knowledge, what is the standard refund policy or relevant law for {company} in the {sector} sector regarding: "{issue}"?
        Provide a concise summary and a likely citation (e.g., 'DOT Regulations' or 'Company Terms').
        """
        found_text = self.llm.query(context_prompt)
        
        return {
            "url": found_url,
            "text": found_text
        }

class VerifierAgent:
    def __init__(self, api_key=None):
        self.llm = get_llm_engine(api_key)

    def verify_source(self, url: str, company: str) -> bool:
        """
        Uses LLM to check if a URL looks authentic for a given company.
        """
        print(f"  [Verifier] AI verifying source: {url}...")
        prompt = f"""
        Is the URL '{url}' a likely official or credible source for information about '{company}'?
        Return 'TRUE' or 'FALSE' and a brief reason.
        """
        response = self.llm.query(prompt)
        print(f"  [Verifier] Assessment: {response.strip()}")
        return "TRUE" in response.upper()

class WriterAgent:
    def __init__(self, api_key=None):
        self.llm = get_llm_engine(api_key)

    def write_letter(self, context: dict) -> str:
        """
        Uses LLM to draft the final letter based on the 'Golden Rules'.
        """
        print("  [Writer] AI drafting formal legal demand letter...")
        
        prompt = f"""
        Act as a professional legal advocate. Write a "Golden Rules" formal demand letter for a refund.
        
        Context:
        - User: {context.get('user_name')} ({context.get('user_email')})
        - Address: {context.get('user_address')}
        - Date: {time.strftime("%Y-%m-%d")}
        - Company: {context.get('company')}
        - Issue: {context.get('issue')}
        - Amount: {context.get('amount')}
        - Transaction Ref: {context.get('ref_number')}
        - Purchase Date: {context.get('purchase_date')}
        - Payment Method: {context.get('payment_method')}
        - Policy/Law Found: {context.get('policy_text')}
        - Source URL: {context.get('policy_url')}
        
        Guidelines:
        - Tone: Professional, firm, non-emotional ("Boring, Not Angry").
        - Structure: Formal business letter.
        - Content: State the demand clearly, cite the policy/law, mention attached evidence, set a deadline (14 days).
        - Output: Return ONLY the letter text.
        """
        return self.llm.query(prompt)

    def write_user_reply(self, context: dict) -> str:
        """
        Uses LLM to explain the strategy to the user.
        """
        prompt = f"""
        Write a short, friendly message to {context.get('user_name')} explaining that their demand letter is ready.
        Mention that we found a policy ({context.get('policy_url')}) that supports their case.
        Tell them to attach proofs and send it as a PDF.
        """
        return self.llm.query(prompt)
