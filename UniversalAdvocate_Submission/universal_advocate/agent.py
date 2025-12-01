import time

def calculate_refund(amount: float, sector: str) -> tuple[float, str]:
    """
    Calculates the refund amount based on the sector and amount.

    Args:
        amount: The original transaction amount.
        sector: The industry sector ('HEALTH', 'TRAVEL', 'RETAIL').

    Returns:
        A tuple containing the final refund amount and a note explaining the calculation.
    """
    sector = sector.upper()
    
    if sector == 'HEALTH':
        # Logic for 'HEALTH': Subtract a standard deductible of $500.
        # If the result is negative, return 0.
        deductible = 500
        final_amount = amount - deductible
        if final_amount < 0:
            final_amount = 0.0
        return final_amount, "Applied Deductible"

    elif sector == 'TRAVEL':
        # Logic for 'TRAVEL': If the amount is over $600, cap the refund at $600.
        if amount > 600:
            return 600.0, "Capped at Regulatory Max"
        else:
            return float(amount), "Full Refund" # Assuming full refund if under cap, though prompt didn't explicitly say, it's implied by the cap logic.

    elif sector == 'RETAIL':
        # Logic for 'RETAIL': Return the full amount.
        return float(amount), "Full Refund"

    else:
        # Default case if sector is unknown, though prompt didn't specify, good practice to handle.
        # For now, let's assume full refund or 0. Let's return 0 with error note to be safe.
        # Actually, let's just return full amount as a fallback or raise error. 
        # The prompt implies these are the only sectors. Let's stick to the prompt's explicit instructions.
        # If no match, maybe return 0? Or just pass through. 
        # Given the prompt "Logic for 'RETAIL': Return the full amount", let's treat unknown like Retail or just 0.
        # I will return 0 for unknown to be safe.
        return 0.0, "Unknown Sector"

def route_case(issue_text: str) -> str:
    """
    Classifies a user's problem into one of four categories based on keywords.

    Args:
        issue_text: The text describing the issue.

    Returns:
        The category name as a string ('HEALTH', 'TRAVEL', 'FINANCE', 'RETAIL').
    """
    issue_text = issue_text.lower()

    # Categories & Keywords
    health_keywords = ['doctor', 'hospital', 'surgery', 'mri', 'bluecross', 'insurance', 'medical']
    travel_keywords = ['flight', 'delay', 'airline', 'indigo', 'hotel', 'train', 'cancel']
    finance_keywords = ['crypto', 'bank', 'transaction', 'fee', 'bitcoin', 'wallet']

    # Check for keywords
    for keyword in health_keywords:
        if keyword in issue_text:
            return "HEALTH"
    
    for keyword in travel_keywords:
        if keyword in issue_text:
            return "TRAVEL"
            
    for keyword in finance_keywords:
        if keyword in issue_text:
            return "FINANCE"

    # Default category
    return "RETAIL"

from agents import ResearcherAgent, VerifierAgent, WriterAgent

class UniversalAdvocate:
    def __init__(self):
        self.researcher = ResearcherAgent()
        self.verifier = VerifierAgent()
        self.writer = WriterAgent()

    def run_agent(self, company: str, amount: float, issue: str, 
                  user_name: str = "Valued Customer", 
                  user_email: str = "customer@example.com",
                  user_address: str = "[Your Address]",
                  purchase_date: str = "[Date]",
                  ref_number: str = "[Reference Number]",
                  payment_method: str = "[Payment Method]") -> dict:
        """
        Executes the step-by-step logic to process a dispute using multiple agents.
        Now accepts detailed user info for the 'Golden Rules' letter.
        """
        print(f"\n--- Starting Universal Advocate for {company} ---")
        print("System Initializing...")
        time.sleep(1)

        # Step 1: Route case
        sector = route_case(issue)
        print(f"Detected Sector: {sector}")
        time.sleep(1)

        # Step 2: Calculate refund
        final_amount, note = calculate_refund(amount, sector)
        print(f"Calculated Refund: ${final_amount} ({note})")
        time.sleep(1)
        
        # Step 3: Research & Verify (New Multi-Agent Flow)
        policy_data = {"url": "N/A", "text": "Standard Regulatory Logic applied."}
        
        # Only research if it's a Travel/Airline case or if requested (simplification for demo)
        if sector == 'TRAVEL' or sector == 'RETAIL':
            found_policy = self.researcher.find_policy(company, sector)
            
            # Verify the found policy
            is_authentic = self.verifier.verify_source(found_policy['url'], company)
            
            if is_authentic:
                policy_data = found_policy
            else:
                print("Using fallback regulatory logic due to unverified source.")

        # Step 4: Generate Professional Letter
        context = {
            "company": company,
            "amount": final_amount,
            "issue": issue,
            "sector": sector,
            "note": note,
            "user_name": user_name,
            "user_email": user_email,
            "user_address": user_address,
            "purchase_date": purchase_date,
            "ref_number": ref_number,
            "payment_method": payment_method,
            "policy_url": policy_data['url'],
            "policy_text": policy_data['text']
        }
        
        letter = self.writer.write_letter(context)
        user_reply = self.writer.write_user_reply(context)
        
        return {
            "letter": letter,
            "user_reply": user_reply
        }
