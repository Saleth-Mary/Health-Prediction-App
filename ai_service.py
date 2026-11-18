
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def generate_health_remarks(glucose, haemoglobin, cholesterol):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please configure your .env file."
        )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000)
    )

    prompt = f"""
    You are an AI health information assistant supporting
    an educational blood test interpretation application.

    Analyse the following patient blood test values:

    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Generate a detailed but easy-to-understand health interpretation
    using the following structure:

    1. GLUCOSE ANALYSIS:
    Explain the reported glucose value and discuss whether it may
    require attention. Do not assume whether the test was fasting
    or post-meal. Mention that interpretation depends on units
    and testing conditions.

    2. HAEMOGLOBIN ANALYSIS:
    Explain the reported haemoglobin value. Mention that its
    interpretation depends on laboratory reference ranges
    and individual patient characteristics.

    3. CHOLESTEROL ANALYSIS:
    Discuss the reported cholesterol value cautiously.
    Do not assume the unit or whether it represents total
    cholesterol, LDL or HDL.

    4. OVERALL HEALTH OBSERVATION:
    Summarise which results may need further attention.
    Avoid making a medical diagnosis.

    5. RECOMMENDATION:
    Suggest appropriate follow-up with a qualified healthcare
    professional and comparison with laboratory reference ranges.

    IMPORTANT INSTRUCTIONS:
    - Do not diagnose any disease.
    - Do not invent measurement units or reference ranges.
    - Do not make unsupported medical conclusions.
    - Clearly explain any limitations caused by missing information.
    - Use professional, simple and understandable English.
    - Keep the interpretation approximately 150-200 words.
    """

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=2048,
                temperature=0.2,
                thinking_config=types.ThinkingConfig(
                    thinking_level="minimal"
                )
            )
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        for candidate in response.candidates or []:
            if candidate.finish_reason == types.FinishReason.MAX_TOKENS:
                raise RuntimeError(
                    "Gemini response was incomplete due to the token limit."
                )

        return response.text.strip()

    except Exception as e:

        raise RuntimeError(
            f"Gemini API request failed: {e}"
        ) from e

    finally:
        client.close()
