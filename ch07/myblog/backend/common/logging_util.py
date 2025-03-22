import json
import logging
from common.localthread_middleware import get_current_user_id, get_txid


def log_event(event_name, log_data, logging_module="django_default", level="INFO"):
    """
    ログメッセージをキャプチャして必要な形式に処理する

    :param event_name: 何千ものログを検索する際に便利なイベント名.
    :param log_data: ログメッセージを含む、シリアライズ可能なデータ. str, dict, list など.
    :param logging_module: デフォルトでは django_default logger を使用.
    :param level: 関数を使用して作成するログのタイプを定義する. INFO, DEBUG, ERROR など. default は INFO.
    """
    logger = logging.getLogger(logging_module)
    try:
        msg = {
            "ev": event_name,
            "data": log_data,
            # txid: 各リクエストの一意なトランザクション ID
            "txid": get_txid(),
        }
        user_id = get_current_user_id()
        if user_id:
            # uid: request から取得したユーザー ID
            msg["uid"] = user_id
        logger.log(msg=json.dumps(msg), level=getattr(logging, level))
    except Exception:
        print("Error")
        return
