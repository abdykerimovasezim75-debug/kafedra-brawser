<!DOCTYPE html>
<html lang="ru">

<head>

    <meta charset="UTF-8">

    <title>Отзывы</title>

    <link rel="stylesheet"
          href="{{ url_for('static', filename='style.css') }}">

</head>

<body>

<div class="review-container">

    <h1>Отзывы</h1>

    <form method="POST"
          enctype="multipart/form-data">

        <textarea
            name="review"
            placeholder="Напишите отзыв">
        </textarea>

        <br><br>

        <input type="file"
               name="photo"
               accept="image/*">

        <br><br>

        <button type="submit">
            Отправить
        </button>

    </form>

</div>

</body>
</html>
