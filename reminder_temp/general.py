from typing import List
from reminder import DutyObject


def find_duty(duty_name: str, dutys: List[DutyObject]):
    for duty in dutys:
        if duty.duty_name == duty_name:
            return duty
    return False


def find_chat_dutys(chat_id: int, dutys: List[DutyObject]):
    chat_dutys = []
    for duty in dutys:
        if duty.chat_id == chat_id:
            chat_dutys.append(duty)
    return chat_dutys
