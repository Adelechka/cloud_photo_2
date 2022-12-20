import telegram
import os
import ydb
import ydb.iam
import json

TOKEN = os.getenv("BOT_TOKEN")
PHOTO_LINK_TEMPLATE = os.getenv("PHOTO_LINK_TEMPLATE")
OBJECT_LINK_TEMPLATE = os.getenv("OBJECT_LINK_TEMPLATE")
ENDPOINT = os.getenv("DB_ENDPOINT")
PATH = os.getenv("DB_PATH")

BOT = telegram.Bot(token=TOKEN)
driver: ydb.Driver

GET_FACE_QUERY = f"""
    PRAGMA TablePathPrefix("{os.getenv("DB_PATH")}");
    SELECT * FROM photo WHERE name is NULL LIMIT 1;
    """
ADD_NAME_TO_LAST_PHOTO_QUERY = f"""
    PRAGMA TablePathPrefix("{os.getenv("DB_PATH")}");
    SELECT * FROM photo WHERE name is NULL LIMIT 1;
    """


def get_driver():
    creds = ydb.iam.MetadataUrlCredentials()
    driver_config = ydb.DriverConfig(
        ENDPOINT, PATH, credentials=creds
    )
    return ydb.Driver(driver_config)


def get_face(chat_id):
    session = driver.table_client.session().create()
    result_sets = session.transaction().execute(GET_FACE_QUERY, commit_tx=True)
    session.closing()
    for row in result_sets[0].rows:
        face_id = row.face_id
        photo_url = PHOTO_LINK_TEMPLATE.format(face_id)
        BOT.send_photo(chat_id=chat_id, photo=photo_url)


def add_name_to_last_photo(name):
    session = driver.table_client.session().create()
    result_sets = session.transaction().execute(ADD_NAME_TO_LAST_PHOTO_QUERY, commit_tx=True)
    face_id = ''
    for row in result_sets[0].rows:
        face_id = row.face_id
    if face_id == '':
        return
    query = f"""
    PRAGMA TablePathPrefix("{os.getenv("DB_PATH")}");
    UPDATE photo SET name = '{name}' WHERE face_id = '{face_id}';
    """
    session.transaction().execute(query, commit_tx=True)
    session.closing()


def find(chat_id, name):
    query = f"""
    PRAGMA TablePathPrefix("{os.getenv("DB_PATH")}");
    SELECT DISTINCT original_id, name FROM photo WHERE name = '{name}';
    """
    session = driver.table_client.session().create()
    result_sets = session.transaction().execute(query, commit_tx=True)
    session.closing()
    if len(result_sets[0].rows) == 0:
        BOT.sendMessage(chat_id, text=f'No photos with {name}')
    for row in result_sets[0].rows:
        object_id = row.original_id
        photo_url = OBJECT_LINK_TEMPLATE.format(object_id)
        BOT.send_photo(chat_id=chat_id, photo=photo_url)


def handler(event, context):
    global driver
    driver = get_driver()
    driver.wait(timeout=5)

    request = event['body']
    update = telegram.Update.de_json(json.loads(request), BOT)

    chat_id = update.message.chat.id
    command = update.message.text.encode('utf-8').decode()

    if command == '/start':
        BOT.sendMessage(chat_id=chat_id, text='Get started!')
        return
    if command == '/get_face':
        get_face(chat_id)
        return
    if command.startswith('/find'):
        args = command.split(' ')
        find(chat_id, args[1])
        return
    add_name_to_last_photo(command)
    BOT.sendMessage(chat_id=chat_id, text=f'Added new name {command}')