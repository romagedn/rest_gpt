
upload chat via chatgpt


pip install -r requirements.tzt


./config.txt

{
	"api_key": "",
}


request

Content-Type: text/plain
body
{
    "asks": list of history ask
    "answers": list of history answer
    "new_chat": new chat message
    "scenario": 描述角色关系，性格，家庭状况，背景等
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

