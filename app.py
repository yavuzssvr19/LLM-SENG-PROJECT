import gradio as gr
import database as db

# Global user session state
current_user = None

def login(username, password):
    """Login function for the interface"""
    global current_user
    success, result = db.authenticate_user(username, password)
    
    if success:
        current_user = result
        # Try to load user profile
        profile_success, profile_data = db.get_user_profile(current_user)
        if profile_success:
            # User has an existing profile, we'll need to populate form in the load_profile function
            return "Login successful!", gr.update(visible=False), gr.update(visible=True)
        else:
            # User doesn't have a profile yet
            return "Login successful! Please complete your profile.", gr.update(visible=False), gr.update(visible=True)
    else:
        return f"Login failed: {result}", gr.update(visible=True), gr.update(visible=False)

def register(username, password, email, confirm_password):
    """Register function for the interface"""
    if password != confirm_password:
        return "Passwords do not match", gr.update(visible=True), gr.update(visible=False)
    
    success, message = db.register_user(username, password, email)
    
    if success:
        return f"{message}. Please login.", gr.update(visible=True), gr.update(visible=False)
    else:
        return message, gr.update(visible=True), gr.update(visible=False)

def logout():
    """Logout function for the interface"""
    global current_user
    current_user = None
    return gr.update(visible=True), gr.update(visible=False)

def save_profile(risk_taker, risk_word, game_show, investment_allocation, 
                market_follow, new_investment, buy_things, finance_reading,
                previous_investments, investment_goal):
    """Save user profile information to the database"""
    if current_user is None:
        return "Error: User not logged in"
    
    # Checkbox groups için özel işlem, liste şeklinde geliyorlar
    previous_investments_list = previous_investments if isinstance(previous_investments, list) else []
    
    success, message = db.save_user_profile(
        current_user,
        risk_taker, risk_word, game_show, investment_allocation,
        market_follow, new_investment, buy_things, finance_reading,
        previous_investments_list, investment_goal
    )
    
    if success:
        return "Profile saved successfully!"
    else:
        return f"Error saving profile: {message}"

def load_profile():
    """Load user profile from database"""
    if current_user is None:
        return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), 
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update())
    
    success, profile_data = db.get_user_profile(current_user)
    
    if not success:
        return (gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), 
                gr.update(), gr.update(), gr.update(), gr.update(), gr.update())
    
    # Return updates for all fields
    return (
        gr.update(value=profile_data.get('risk_taker', 'Cautious')),
        gr.update(value=profile_data.get('risk_word', 'Uncertainty')),
        gr.update(value=profile_data.get('game_show', '$1,000 in cash')),
        gr.update(value=profile_data.get('investment_allocation', '60% in low-risk, 30% in medium-risk, 10% in high-risk investments')),
        gr.update(value=profile_data.get('market_follow', 'Weekly')),
        gr.update(value=profile_data.get('new_investment', 'Research thoroughly before investing')),
        gr.update(value=profile_data.get('buy_things', 'Neutral')),
        gr.update(value=profile_data.get('finance_reading', 'Neutral')),
        gr.update(value=profile_data.get('previous_investments', [])),
        gr.update(value=profile_data.get('investment_goal', 'Long-term savings'))
    )

# Mock chatbot functions
def education_chatbot(message, history):
    """Placeholder for education chatbot"""
    return history + [[message, "This is the Education Chatbot. It will be implemented soon!"]]

def advisor_chatbot(message, history):
    """Placeholder for advisor and analyzer chatbot"""
    return history + [[message, "This is the Advisor & Analyzer Chatbot. It will be implemented soon!"]]

# Create custom CSS for larger text with green theme
custom_css = """
:root {
    --primary-color: #2E7D32;
    --secondary-color: #4CAF50;
    --light-green: #81C784;
    --dark-green: #1B5E20;
    --text-color: #212121;
    --light-text: #FFFFFF;
}

.larger-text label {
    font-size: 22px !important;
    font-weight: bold !important;
    color: var(--dark-green) !important;
}

.larger-text .prose h1 {
    font-size: 36px !important;
    font-weight: bold !important;
    color: var(--primary-color) !important;
}

.larger-text .prose h2 {
    font-size: 32px !important;
    font-weight: bold !important;
    color: var(--primary-color) !important;
}

.larger-text .prose p {
    font-size: 20px !important;
    color: var(--text-color) !important;
}

.larger-text input, .larger-text select {
    font-size: 20px !important;
    padding: 12px !important;
    border-color: var(--secondary-color) !important;
}

.larger-text button {
    font-size: 22px !important;
    padding: 12px 24px !important;
    font-weight: bold !important;
    background-color: var(--primary-color) !important;
    color: var(--light-text) !important;
}

.larger-text button:hover {
    background-color: var(--secondary-color) !important;
}

/* Override Gradio defaults for better visibility */
.dark .larger-text label, .dark .larger-text .prose h1, .dark .larger-text .prose h2 {
    color: var(--light-green) !important;
}

.dark .larger-text .prose p {
    color: #E0E0E0 !important;
}

.dark .larger-text input, .dark .larger-text select {
    background-color: #1B5E20 !important;
    color: white !important;
    border-color: var(--light-green) !important;
}

/* Make dropdown options more readable */
.larger-text select option {
    font-size: 20px !important;
    padding: 10px !important;
}
"""

# Create the main application
with gr.Blocks(title="FINSENTIO", css=custom_css, theme=gr.themes.Soft()) as app:
    with gr.Blocks(elem_classes=["larger-text"]):
        gr.Markdown("# FINSENTIO")
        
        # Create dashboard interface
        with gr.Group(visible=False) as dashboard:
            gr.Markdown("# Welcome to your Dashboard")
            
            with gr.Tabs():
                with gr.TabItem("Profile"):
                    gr.Markdown("## User Risk Profile Assessment")
                    gr.Markdown("Please answer the following questions to help us understand your investment preferences and risk tolerance.")
                    
                    # Question 1
                    with gr.Row():
                        with gr.Column():
                            risk_taker = gr.Radio(
                                label="1. How would your best friend describe you as a risk taker?",
                                choices=[
                                    "A real gambler",
                                    "Willing to take risks after completing adequate research",
                                    "Cautious",
                                    "A real risk avoider"
                                ],
                                value="Cautious",
                                scale=2
                            )
                    
                    # Question 2
                    with gr.Row():
                        with gr.Column():
                            risk_word = gr.Radio(
                                label="2. When you think of the word \"risk\", which of the following words comes to mind first?",
                                choices=[
                                    "Loss",
                                    "Uncertainty",
                                    "Opportunity",
                                    "Thrill"
                                ],
                                value="Uncertainty",
                                scale=2
                            )
                    
                    # Question 3
                    with gr.Row():
                        with gr.Column():
                            game_show = gr.Radio(
                                label="3. You are on a TV game show and can choose one of the following. Which would you take?",
                                choices=[
                                    "$1,000 in cash",
                                    "A 50% chance at winning $5,000",
                                    "A 25% chance at winning $10,000",
                                    "A 5% chance at winning $100,000"
                                ],
                                value="$1,000 in cash",
                                scale=2
                            )
                    
                    # Question 4
                    with gr.Row():
                        with gr.Column():
                            investment_allocation = gr.Radio(
                                label="4. If you had to invest $20,000, which of the following allocations would you find most appealing?",
                                choices=[
                                    "60% in low-risk, 30% in medium-risk, 10% in high-risk investments",
                                    "30% in low-risk, 30% in medium-risk, 40% in high-risk investments",
                                    "10% in low-risk, 40% in medium-risk, 50% in high-risk investments"
                                ],
                                value="60% in low-risk, 30% in medium-risk, 10% in high-risk investments",
                                scale=2
                            )
                    
                    # Question 5
                    with gr.Row():
                        with gr.Column():
                            market_follow = gr.Radio(
                                label="5. How often do you follow financial markets?",
                                choices=[
                                    "Daily",
                                    "Weekly",
                                    "Occasionally",
                                    "Never"
                                ],
                                value="Weekly",
                                scale=2
                            )
                    
                    # Question 6
                    with gr.Row():
                        with gr.Column():
                            new_investment = gr.Radio(
                                label="6. What would you do when you hear about a new investment opportunity?",
                                choices=[
                                    "Immediately jump in",
                                    "Research thoroughly before investing",
                                    "Ask others first, then decide",
                                    "Wait and observe over time"
                                ],
                                value="Research thoroughly before investing",
                                scale=2
                            )
                    
                    # Question 7
                    with gr.Row():
                        with gr.Column():
                            buy_things = gr.Radio(
                                label="7. I rarely buy things I don't need.",
                                choices=[
                                    "Agree",
                                    "Neutral",
                                    "Disagree"
                                ],
                                value="Neutral",
                                scale=2
                            )
                    
                    # Question 8
                    with gr.Row():
                        with gr.Column():
                            finance_reading = gr.Radio(
                                label="8. I like to read about finance and the economy.",
                                choices=[
                                    "Agree",
                                    "Neutral",
                                    "Disagree"
                                ],
                                value="Neutral",
                                scale=2
                            )
                    
                    # Question 9
                    with gr.Row():
                        with gr.Column():
                            previous_investments = gr.CheckboxGroup(
                                label="9. Which of the following have you invested in before? (You can choose more than one)",
                                choices=[
                                    "Stocks",
                                    "Cryptocurrency",
                                    "Foreign currencies",
                                    "Gold or other commodities",
                                    "Fixed deposit accounts",
                                    "I have never invested"
                                ],
                                value=[],
                                scale=2
                            )
                    
                    # Question 10
                    with gr.Row():
                        with gr.Column():
                            investment_goal = gr.Radio(
                                label="10. What is your main goal for investing?",
                                choices=[
                                    "Short-term profit",
                                    "Long-term savings",
                                    "Retirement planning",
                                    "Wealth preservation"
                                ],
                                value="Long-term savings",
                                scale=2
                            )
                    
                    # Save button
                    with gr.Row():
                        save_button = gr.Button("Save Profile", size="lg", variant="primary")
                    profile_message = gr.Markdown("")
                    
                    # Connect save button to function
                    save_button.click(
                        fn=save_profile,
                        inputs=[
                            risk_taker, risk_word, game_show, investment_allocation,
                            market_follow, new_investment, buy_things, finance_reading,
                            previous_investments, investment_goal
                        ],
                        outputs=profile_message
                    )
                
                with gr.TabItem("Education Chatbot"):
                    gr.Markdown("## Financial Education Chatbot")
                    gr.Markdown("Ask any questions about financial terms, concepts, or strategies to improve your knowledge!")
                    
                    # Education chatbot interface
                    education_chat = gr.Chatbot(
                        label="Chat History",
                        height=400,
                        value=[["System", "Welcome to the Financial Education Chatbot! How can I help you learn today?"]]
                    )
                    education_msg = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask me anything about finance...",
                        scale=7
                    )
                    education_submit = gr.Button("Ask", scale=1, variant="primary")
                    education_clear = gr.Button("Clear Chat", scale=1)
                    
                    # Connect chatbot components
                    education_submit.click(
                        fn=education_chatbot,
                        inputs=[education_msg, education_chat],
                        outputs=[education_chat],
                        api_name="education_chat"
                    )
                    education_clear.click(lambda: [], None, education_chat)
                
                with gr.TabItem("Adviser & Analyzer"):
                    gr.Markdown("## Financial Adviser & Analyzer")
                    gr.Markdown("Get personalized financial advice and analysis based on your profile and market conditions.")
                    
                    # Adviser chatbot interface
                    adviser_chat = gr.Chatbot(
                        label="Chat History",
                        height=400,
                        value=[["System", "Welcome to your personalized Financial Adviser! How can I assist you today?"]]
                    )
                    adviser_msg = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask for financial advice or market analysis...",
                        scale=7
                    )
                    adviser_submit = gr.Button("Ask", scale=1, variant="primary")
                    adviser_clear = gr.Button("Clear Chat", scale=1)
                    
                    # Connect chatbot components
                    adviser_submit.click(
                        fn=advisor_chatbot,
                        inputs=[adviser_msg, adviser_chat],
                        outputs=[adviser_chat],
                        api_name="adviser_chat"
                    )
                    adviser_clear.click(lambda: [], None, adviser_chat)
            
            # Logout button
            with gr.Row():
                logout_button = gr.Button("Logout", size="lg", variant="stop")
        
        # Create auth interface
        with gr.Group(visible=True) as auth_interface:
            with gr.Tabs():
                with gr.TabItem("Login"):
                    username_login = gr.Textbox(label="Username", scale=2)
                    password_login = gr.Textbox(label="Password", type="password", scale=2)
                    with gr.Row():
                        login_button = gr.Button("Login", size="lg", variant="primary")
                    login_message = gr.Markdown("")
                
                with gr.TabItem("Register"):
                    username_register = gr.Textbox(label="Username", scale=2)
                    email_register = gr.Textbox(label="Email", scale=2)
                    password_register = gr.Textbox(label="Password", type="password", scale=2)
                    confirm_password = gr.Textbox(label="Confirm Password", type="password", scale=2)
                    with gr.Row():
                        register_button = gr.Button("Register", size="lg", variant="primary")
                    register_message = gr.Markdown("")
        
        # Connect the buttons to functions
        login_button.click(
            fn=login,
            inputs=[username_login, password_login],
            outputs=[login_message, auth_interface, dashboard]
        ).then(
            fn=load_profile,
            inputs=None,
            outputs=[
                risk_taker, risk_word, game_show, investment_allocation,
                market_follow, new_investment, buy_things, finance_reading,
                previous_investments, investment_goal
            ]
        )
        
        register_button.click(
            fn=register,
            inputs=[username_register, password_register, email_register, confirm_password],
            outputs=[register_message, auth_interface, dashboard]
        )
        
        logout_button.click(
            fn=logout,
            outputs=[auth_interface, dashboard]
        )

if __name__ == "__main__":
    app.launch()