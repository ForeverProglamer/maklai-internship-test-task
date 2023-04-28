from itertools import islice

from fastapi import FastAPI, HTTPException, status

from app.paraphrase import paraphrase_sentence, DeserializationError
from app.schema import ParaphraseModel, ParaphraseResponse

app = FastAPI()


@app.get('/paraphrase')
async def paraphrase(
    tree: str,
    limit: int | None = 20
) -> ParaphraseResponse[ParaphraseModel]:
    try:
        paraphrases = [
            ParaphraseModel(tree=str(paraphrased)) 
            for paraphrased in islice(paraphrase_sentence(tree), limit)
        ]
    except DeserializationError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Invalid serialized tree format given'
        )
    return ParaphraseResponse(paraphrases=paraphrases)
