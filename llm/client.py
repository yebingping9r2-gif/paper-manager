# llm/client.py
import requests
from config.llm_config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from config.logger import logger
from utils.exceptions import PaperManagerError

def chat_with_llm(user_question: str) -> str:
    """
    调用大模型单轮对话，返回纯文本回答
    :param user_question: 用户输入的问题
    """
    # 标准的消息格式：system设定人设 + user提问
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "你是专业的科研助手，回答简洁准确，逻辑清晰。"},
            {"role": "user", "content": user_question}
        ],
        "temperature": 0.7,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}"
    }

    try:
        logger.info(f"调用大模型，问题摘要：{user_question[:60]}...")
        response = requests.post(
            LLM_BASE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()  # 状态码非200自动触发异常
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        logger.info("大模型调用成功")
        return answer

    except requests.exceptions.Timeout:
        logger.error("大模型调用超时")
        raise PaperManagerError("模型响应超时，请稍后重试")
    except requests.exceptions.RequestException as e:
        logger.error(f"大模型调用失败：{str(e)}")
        raise PaperManagerError(f"模型调用失败：{str(e)}")
    except KeyError:
        logger.error("大模型返回格式异常")
        raise PaperManagerError("模型返回数据格式异常")
