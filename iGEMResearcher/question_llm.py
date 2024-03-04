import openai

def refine_question(content):
    # OpenAI API key configuration
    openai.api_key = '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'

    # Enhanced prompt to include specific categories and search term
    prompt = f"Please refine the following question by making it more specific, including relevant details such as region, track, year, kind, and section, and any specific search terms:\n\n{content}"

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Refine the question to be more specific by including details like region, track, year, kind, section, and any search terms."},
            {"role": "user", "content": prompt},
        ]
    )

    # Output the refined question text
    refined_question = response['choices'][0]['message']['content']
    return refined_question.strip()
