from openai import OpenAI

client = OpenAI(
    api_key="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"
)

def get_response(user_message):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
           {
    "role": "system",
    "content": """
    Ты бот-помощник кафедры компьютерной лингвистики.
    Отвечай кратко, максимум 2-3 предложения.
    Если вопрос о кафедре, давай только основную информацию.
    Не используй длинные списки и большие объяснения.
    """
},
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    if "кафедра" in user_message.lower():
        return "Кафедра компьютерной лингвистики занимается изучением языка и современных цифровых технологий. Мы готовим специалистов в области  обработки текста, искусственного интеллекта и анализа данных"

    if "направления" in user_message.lower():
        return "Основные направления: Обработка естественного языка NLP, машинный перевод, искусственный интеллект и анализ данных."

    if "поступить" in user_message.lower():
        return "Поступление осуществляется через приёмную комиссию института. Подробную информацию о поступлении, необходимых документах и сроках подачи можно узнать по контактным данным"
    return response.choices[0].message.content