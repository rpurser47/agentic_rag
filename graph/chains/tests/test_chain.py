from dotenv import load_dotenv

from pprint import pprint

load_dotenv()

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from graph.chains.generation import generation_chain
from graph.chains.hallucination_grader import (GradeHallucinations, hallucination_grader)
from graph.chains.router import question_router, RouteQuery
from ingestion import retriever

def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    docs =  retriever.invoke(question)
    doc_txt = docs[1].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "yes"

def test_retrieval_grader_answer_no() -> None:
    question = "how to make pizza"
    docs =  retriever.invoke(question)
    doc_txt = docs[1].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "no"

def test_generation_chain() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question": question})
    pprint(generation)

def test_hallucination_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"context": docs, "question": question})
    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )
    assert res.binary_score

def test_hallucination_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs,
         "generation": "in order to make pizza, we first need to start with the dough."}
    )
    assert not res.binary_score

def test_router_vectorstore() -> None:
    question = "agent memory"
    res = RouteQuery = question_router.invoke({"question": question})
    assert res.datasource == "vectorstore"
    
def test_router_websearch() -> None:
    question = "how to make pizza"
    res = RouteQuery = question_router.invoke({"question": question})
    assert res.datasource == "websearch"