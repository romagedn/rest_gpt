
upload chat via chatgpt


pip install -r requirements.tzt


./config.txt

{
	"api_key": "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",
}


request

Content-Type: text/plain
body
{
    "asks": list of history ask
    "answers": list of history answer
    "new_chat": new chat message
    "role":
    {
        "relationship": 父亲 \ 母亲 \ 哥哥 \ 弟弟 \ 姐姐 \ 妹妹等，表示和user的关系
        "family": 描述家庭状况，有什么成员，相互关系等
        "character": 描述数字人性格特点
    }
}


response

{
    "status": True / False,
    "answer": new chat response
    "asks": updated asks, used for future chat
    "answers": updated answers, used for future chat
}


port
13131

