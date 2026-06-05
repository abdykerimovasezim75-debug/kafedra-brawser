from openai import OpenAI

client = OpenAI(
    api_key="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"
)


def get_response(user_message):

    if "кафедра" in user_message.lower():
        return "Кафедра компьютерной лингвистики занимается изучением языка и современных цифровых технологий.Мы готовим специалистов в области обработки текста, искусственного интеллекта и анализа данных."

    if "направления" in user_message.lower():
        return "Основные направления: Обработка естественного языка (NLP) Машинный перевод Искусственный интеллект Анализ данных и текстов"

    if "поступить" in user_message.lower():
        return "Поступление осуществляется через приёмную комиссию института. Подробную информацию о поступлении, необходимых документах и сроках подачи можно узнать по контактным данным кафедры."

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

    return response.choices[0].message.content
