from concurrent.futures import ThreadPoolExecutor

from transformers import BertTokenizer, BertForSequenceClassification

from app.infrastructure.dao.polls.poll import PollDAO
from app.infrastructure.dao.polls.poll_variant import PollVariantDAO
from app.infrastructure.dao.toxicity import ToxicityDAO
from app.infrastructure.dao.user import UserDAO
from app.infrastructure.database import DatabaseWrapper


class ToxicContainer:

    def __init__(self):
        self._tokenizer: None | BertTokenizer = None
        self._model: None | BertForSequenceClassification = None
        # TODO: finalize
        self._poll = ThreadPoolExecutor(max_workers=10)

    def get_model(self) -> BertForSequenceClassification:
        if not self._model:
            self._model = BertForSequenceClassification.from_pretrained(
                "SkolkovoInstitute/russian_toxicity_classifier"
            )
        return self._model

    def get_tokenizer(self) -> BertTokenizer:
        if not self._tokenizer:
            self._tokenizer = BertTokenizer.from_pretrained(
                "SkolkovoInstitute/russian_toxicity_classifier"
            )
        return self._tokenizer

    def get_pool(self) -> ThreadPoolExecutor:
        return self._poll


class DAOContainer:

    def __init__(self, db: DatabaseWrapper):
        self._db = db
        self.toxicity = ToxicityDAO(self._db)
        self.users = UserDAO(self._db)
        self.polls = PollDAO(self._db)
        self.poll_variants = PollVariantDAO(self._db)

    async def finalize(self):
        await self._db.close()


class AppContainer:
    def __init__(self, db: DatabaseWrapper, toxic_container: ToxicContainer):
        self.toxic_container = toxic_container
        self.dao = DAOContainer(db)

    async def finalize(self):
        await self.dao.finalize()

    @classmethod
    async def create(cls):
        db = await DatabaseWrapper.create("../../db.sqlite")
        toxic_container = ToxicContainer()
        return cls(db, toxic_container)
