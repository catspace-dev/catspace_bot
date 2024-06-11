import asyncio
from concurrent.futures import ThreadPoolExecutor

import torch
from transformers import BertTokenizer, BertForSequenceClassification

from app.infrastructure.dao.toxicity import ToxicityDAO


class ToxicClassificationService:

    def __init__(
        self,
        tokenizer: BertTokenizer,
        model: BertForSequenceClassification,
        dao: ToxicityDAO,
        pool: ThreadPoolExecutor,
    ):
        self._tokenizer = tokenizer
        self._model = model
        self._dao = dao
        self._pool = pool

    def _classify(self, text: str) -> float:
        batch = self._tokenizer.encode(text, return_tensors="pt")
        outputs = self._model(batch)
        logits = outputs[0]
        prob = torch.nn.functional.softmax(logits, dim=1)[:, 1]
        return float(prob.cpu().detach().numpy()[0])

    async def execute(self, user_id: int, chat_id: int, text: str):
        coro = asyncio.get_running_loop().run_in_executor(self._pool, self._classify, text)
        result = await coro
        await self._dao.add(user_id, chat_id, result)


class ToxicStatsService:

    def __init__(self, dao: ToxicityDAO):
        self._dao = dao

    async def execute(self, chat_id: int) -> str:
        users = await self._dao.get_stats(chat_id)
        message = "🤮 ТОП ПЯТЬ ТОКСИКОВ, ГАСИТЕ ИХ:\n\n"
        for i, user in enumerate(users, 1):
            message += f"{i}. {user}\n"
        return message


