import streamlit as st
import google.generativeai as genai

# Configure the Generative AI API
genai.configure(api_key="AIzaSyBe6xhWh50TpHsS-tW0ilbNq2nFvs0FOAk")

# Updated Prompt Template for House Price Prediction
input_prompt = """
You are an AI assistant that predicts house prices based on user-provided details. The user will input the following information:
1. Location (city, zip code, or neighborhood)
2. Total square footage
3. Number of bedrooms
4. Number of bathrooms
5. Year built
6. Lot size
7. Garage (yes/no)
8. Additional features (e.g., pool, garden, etc.)

Your task is to:
1. Predict the approximate price of the house in both Indian Rupees (INR) and United States Dollars (USD).
2. Use the most recent exchange rate (1 USD ≈ 83 INR) to provide the conversion.
3. Provide a brief explanation of how the prediction is made.
4. Highlight the key factors influencing the price.
5. Suggest 2–3 ways the user could increase the value of the house.

Use recent real estate trends and market insights from both Indian and international markets to provide accurate predictions and recommendations.
"""


# Function to get predictions and explanations using Generative AI
def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    if hasattr(response.candidates[0], "content") and hasattr(response.candidates[0].content, "parts"):
        return response.candidates[0].content.parts[0].text
    else:
        return None

# Streamlit UI
st.title("House Price Prediction App")

st.write("Enter the details of the house to get a predicted price and recommendations.")

# Input fields for house details
location = st.text_input("Location (City, Zip Code, Neighborhood):")
square_footage = st.number_input("Total Square Footage:", min_value=0, step=10)
bedrooms = st.number_input("Number of Bedrooms:", min_value=0, step=1)
bathrooms = st.number_input("Number of Bathrooms:", min_value=0, step=1)
year_built = st.number_input("Year Built:", min_value=1800, max_value=2025, step=1)
lot_size = st.number_input("Lot Size (in acres):", min_value=0.0, step=0.01)
garage = st.radio("Garage:", ("Yes", "No"))
additional_features = st.text_area("Additional Features (e.g., pool, garden):")

# Button to predict the house price
# Button to predict the house price
if st.button("Predict Price"):
    # Combine user inputs into the prompt
    prompt = f"""
    {input_prompt}

    House Details:
    - Location: {location}
    - Total Square Footage: {square_footage}
    - Number of Bedrooms: {bedrooms}
    - Number of Bathrooms: {bathrooms}
    - Year Built: {year_built}
    - Lot Size: {lot_size} acres
    - Garage: {garage}
    - Additional Features: {additional_features}
    """

    try:
        # Get response from Generative AI
        response = get_gemini_response(prompt)

        if response:
            # Assuming the AI provides the price in both INR and USD
            st.subheader("Predicted Price and Insights")
            st.write(response)
        else:
            st.error("Unexpected response format. Please try again.")
    except Exception as e:
        st.error(f"Error generating prediction: {e}")

