from environs import Env

# environs use library
env = Env()
env.read_env()

# .env file read
BOT_TOKEN = env.str("BOT_TOKEN")
BASIC_API = env.str("BASIC_API")

START_TEXT = "Ассалому алайкум!\nОилавий тадбиркорликни ривожлантириш дастурлари " \
             "Ягона электрон платформаси телеграм ботига хуш келибсиз!\n" \
             "Қуйидагилардан бирини юборинг:\n\n- Ариза рақам\n- Паспорт серия ва рақами\n- ЖШШИР\n- СТИР"

def check_message(msg: str):
    if len(msg) < 9 and msg.isdigit(): return 'app'
    elif len(msg) == 9 and not msg.isdigit(): return 'pass'
    elif len(msg) == 14 and msg.isdigit(): return 'pinfl'
    elif len(msg) == 9 and msg.isdigit(): return 'tin'
    else: return 'error'

def last_notify(data: dict) -> str:
    text = f"<b>Охирги ариза ҳолати</b>: {get_doc_status(data['app_status'])},"  \
           f"\nариза рақами: {data['app_id']}  {get_date(data['app_date'])}\n"   \
           f"\n<b>Тавсиянома</b>: {for_recom(data['app_status'])},\n"            \
           f"\n<b>Кредит шартнома</b>: {con_supp_inv(data['con_status'])}, "     \
           f"{get_id(data['con_id'])}  {get_date(data['con_date'])}\n"           \
           f"\n<b>Таьминот шартнома</b>: {con_supp_inv(data['supp_status'])}, "  \
           f"{get_id(data['supp_id'])}  {get_date(data['supp_date'])}\n"         \
           f"\n<b>Ҳисоб-фактура</b>: {con_supp_inv(data['inv_status'])}, "       \
           f"{get_id(data['inv_id'])}  {get_date(data['inv_date'])}\n"           \
           f"\n<b>Мониторинг</b>: {for_act(data['act_status'])}, "               \
           f"{get_id(data['act_id'])}  {get_date(data['act_date'])}\n"           \
           f"\n<b>Кредит</b>: {for_pay_docs(data['pay_status'])}, "              \
           f"{get_id(data['pay_id'])}  {get_date(data['pay_date'])}\n"           \
           f"\nҚуйидаги эски аризалар"
    return text

def notify(data: dict) -> str:
    text = f"<b>Ариза ҳолати</b>: {get_doc_status(data['app_status'])},"         \
           f"\nариза рақами: {data['app_id']}  {get_date(data['app_date'])}\n"   \
           f"\n<b>Тавсиянома</b>: {for_recom(data['app_status'])},\n"            \
           f"\n<b>Кредит шартнома</b>: {con_supp_inv(data['con_status'])}, "     \
           f"{get_id(data['con_id'])}  {get_date(data['con_date'])}\n"           \
           f"\n<b>Таьминот шартнома</b>: {con_supp_inv(data['supp_status'])}, "  \
           f"{get_id(data['supp_id'])}  {get_date(data['supp_date'])}\n"         \
           f"\n<b>Ҳисоб-фактура</b>: {con_supp_inv(data['inv_status'])}, "       \
           f"{get_id(data['inv_id'])}  {get_date(data['inv_date'])}\n"           \
           f"\n<b>Мониторинг</b>: {for_act(data['act_status'])}, "               \
           f"{get_id(data['act_id'])}  {get_date(data['act_date'])}\n"           \
           f"\n<b>Кредит</b>: {for_pay_docs(data['pay_status'])}, "              \
           f"{get_id(data['pay_id'])}  {get_date(data['pay_date'])}"
    return text

def get_doc_status(app_status):
    if app_status == 'CREATED': return 'Тасдиқланмаган'
    elif app_status == 'CANCELED': return 'Аризачи томонидан бекор қилинган'
    elif app_status == 'SCORE_IN_PROCESS': return 'Скоринг жараёнида'
    elif app_status == 'SCORE_REJECTED': return 'Рад этилган (скоринг)'
    elif app_status == 'AT_HOKIM': return 'Ко`риб чиқилмоқда'
    elif app_status == 'IN_VIEWING_QUEUE': return 'Кўриб чиқиш учун навбатда'
    elif app_status == 'HOKIM_REJECTED': return 'Рад этилган'
    elif app_status == 'AT_ACCUMULATION': return 'Жамг’арма ко’риб чиқмоқда'
    elif app_status == 'ACCUMULATION_REJECTED': return 'Жамг’арма рад этган'
    elif app_status == 'AT_DISTRICT': return 'Туман марказида'
    elif app_status == 'DISTRICT_REJECTED': return 'Рад этилган (туман)'
    elif app_status == 'AT_AREA': return 'Ҳудуд марказида'
    elif app_status == 'AREA_REJECTED': return 'Рад этилган (ҳудуд)'
    elif app_status == 'BANK_REJECTED': return 'Рад этилган (банк)'
    elif app_status == 'IN_QUEUE': return 'Навбат кутилмоқда'
    elif app_status == 'ACCEPTED': return 'Тавсиянома берилган'
    else: return ''

def for_pay_docs(pay_status):
    if pay_status != 'null': return 'Ажратилган'
    else: return 'Ажратилмаган'

def for_recom(app_status):
    if app_status == 'ACCEPTED': return 'Берилган'
    else: return 'Берилмаган'

def for_act(act_status):
    if act_status == 'ACCEPTED': return 'Қилинган'
    elif act_status == 'CREATED': return 'Тасдиқланмаган'
    elif act_status == 'CANCELED': return 'Бекор қилинган'
    elif act_status == 'REJECTED': return 'Рад етилган'
    elif act_status == 'SENDING_AGENCY': return 'Агентликка юборилган'
    else: return 'Қилинмаган'

def con_supp_inv(status):
    if status == 'FULL_SIGNED': return 'Имзоланган'
    elif status == 'REJECTED': return 'Рад етилган'
    elif status == 'CANCELED': return 'Бекор қилинган'
    elif status == 'CREATED': return 'Тасдиқланмаган'
    elif status == 'IN_PROCESS': return 'Жараёнда'
    else: return 'Имзоланмаган'

def get_id(id):
    if id == None: return ''
    else: return f'№ {id}'

def get_date(date):
    if date == None: return ''
    else: return f'санаси {date}'