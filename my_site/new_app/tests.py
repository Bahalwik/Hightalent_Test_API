import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import Question, Answer


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestQuestionAPI:
    """Тесты для API вопросов."""

    def test_create_question(self, client):
        """Тест создания вопроса."""

        response = client.post('/api/questions/', {'text': 'Новый тестовый вопрос?'})
        assert response.status_code == status.HTTP_201_CREATED
        assert Question.objects.count() == 1
        assert response.data['text'] == 'Новый тестовый вопрос?'

    def test_list_questions(self, client):
        """Тест получения списка вопросов."""

        Question.objects.create(text='Вопрос 1')
        Question.objects.create(text='Вопрос 2')
        response = client.get('/api/questions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_question(self, client):
        """Тест получения одного вопроса с ответами"""

        question = Question.objects.create(text='Вопрос с ответами')
        Answer.objects.create(question=question, user_id='user1', text='Ответ 1')
        response = client.get(f'/api/questions/{question.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == question.text
        assert len(response.data['answers']) == 1
        assert response.data['answers'][0]['text'] == 'Ответ 1'

    def test_delete_question_cascades(self, client):
        """Тест удаления вопроса"""

        question = Question.objects.create(text='Вопрос на удаление')
        Answer.objects.create(question=question, user_id='user1', text='Ответ для удаления')
        assert Question.objects.count() == 1
        assert Answer.objects.count() == 1

        response = client.delete(f'/api/questions/{question.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Question.objects.count() == 0
        assert Answer.objects.count() == 0


@pytest.mark.django_db
class TestAnswerAPI:
    """Тесты для API ответов."""

    @pytest.fixture
    def question(self):
        """Фикстура для создания вопроса"""

        return Question.objects.create(text='Вопрос для ответов')

    def test_create_answer(self, client, question):
        """Тест создания ответа"""

        url = f'/api/questions/{question.id}/answers/'
        data = {'user_id': 'test_user', 'text': 'Тестовый ответ'}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Answer.objects.count() == 1
        assert response.data['text'] == 'Тестовый ответ'

    def test_create_answer_for_nonexistent_question(self, client):
        """Тест: нельзя создать ответ для несуществующего вопроса."""

        url = '/api/questions/999/answers/'
        data = {'user_id': 'test_user', 'text': 'Ответ в никуда'}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_answer(self, client, question):
        """Тест удаления ответа."""

        answer = Answer.objects.create(question=question, user_id='user1', text='Ответ на удаление')
        assert Answer.objects.count() == 1
        response = client.delete(f'/api/answers/{answer.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Answer.objects.count() == 0
