
# Maintenance Chatbot

This project is a Streamlit-based chatbot designed to assist with maintenance questions for industrial products. The chatbot leverages DeepSeek OpenAI's language model to provide structured and accurate answers based on provided maintenance documents and sensor data.

## Features

- **Multiple Modes**: Choose between different modes for the chatbot:

  - **LLM**: Basic language model interaction.
  
  - **LLM with context**: Provides answers using maintenance documents.
  
  - **LLM with context and AI agents**: Uses both maintenance documents and sensor data for more comprehensive answers.
  
- **Structured Responses**: Answers are provided in a structured, enumerated format.

- **Document Integration**: Reads and integrates information from maintenance documents and sensor data files.


## Setup

1. **Clone the repository**:

    ```bash
    git clone git@github.com:CIMK-HUB/maintanance-chatbot-poc.git
    cd maintenance-chatbot-poc
    ```

2. **Install dependencies**:

    ```bash
    poetry install --no-root
    ```

3. **Set up environment variables**:

    - Create a `.env` file in the root directory.
    
    - Add your DeepSeek API key:
        ```
        DEEPSEEK_API_KEY=your_deepseek_api_key
        ```

4. **Prepare data files**:

    - Place your maintenance documents in `data/extracted_pages.md`.
    
    - Place your sensor data in `data/Realistic_Pt100_Sensor_Data.txt`.


## Usage
Run the Streamlit app:

```bash
streamlit run app.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.