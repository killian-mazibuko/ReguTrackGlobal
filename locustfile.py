import random
import time

from locust import HttpUser, between, task


class ChatUser(HttpUser):
    wait_time = between(5, 20)

    @task
    def ask_question(self):
        self.client.get(
            "/",
            name="home",
        )
        time.sleep(self.wait_time())
        first_question = random.choice(
            [
                "What does that South African law say about Data Protection?",
                "What does the US law say on Money Laundering?",
                "Which law protects UK residents with regards to Data Protection?",
                "How is Data Protection administered in Nigeria?",
            ]
        )

        response = self.client.post(
            "/chat",
            name="initial chat",
            json={
                "messages": [
                    {
                        "content": first_question,
                        "role": "user",
                    },
                ],
                "context": {
                    "overrides": {
                        "retrieval_mode": "hybrid",
                        "semantic_ranker": True,
                        "semantic_captions": False,
                        "top": 3,
                        "suggest_followup_questions": True,
                    },
                },
            },
        )
        time.sleep(self.wait_time())
        # use one of the follow up questions.
        follow_up_question = random.choice(response.json()["context"]["followup_questions"])
        result_message = response.json()["message"]["content"]

        self.client.post(
            "/chat",
            name="follow up chat",
            json={
                "messages": [
                    {"content": first_question, "role": "user"},
                    {
                        "content": result_message,
                        "role": "assistant",
                    },
                    {"content": follow_up_question, "role": "user"},
                ],
                "context": {
                    "overrides": {
                        "retrieval_mode": "hybrid",
                        "semantic_ranker": True,
                        "semantic_captions": False,
                        "top": 3,
                        "suggest_followup_questions": False,
                    },
                },
            },
        )
