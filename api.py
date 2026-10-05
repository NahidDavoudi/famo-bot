"""کلاینت API فامو — تنها جایی که بات با بک‌اند حرف می‌زند.

فرض‌ها (مسیرها را با Famo Unified API هماهنگ کن):
- احراز هویت بات با هدر X-Bot-Key
- پاسخ‌ها با envelope: {success, data, error}
- درخواست‌ها multipart/form-data (برای ارسال فایل)
"""

import httpx

from config import config


class ApiError(Exception):
    pass


_client: httpx.AsyncClient | None = None


def _http() -> httpx.AsyncClient:
    # کلاینت باید روی همان حلقه مشترک ساخته شود (اینجا داخل coroutine صدا زده می‌شود)
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=config.API_BASE_URL,
            headers={"X-Bot-Key": config.API_KEY},
            timeout=20,
        )
    return _client


async def _call(method, path, data=None, file=None, params=None, allow_404=False):
    files = {"file": file} if file else None
    r = await _http().request(method, path, data=data, files=files, params=params)
    if r.status_code == 404 and allow_404:
        return None
    try:
        body = r.json()
    except ValueError:
        raise ApiError(f"پاسخ نامعتبر از API (HTTP {r.status_code})")
    if not body.get("success"):
        err = body.get("error")
        msg = err.get("message") if isinstance(err, dict) else err
        raise ApiError(msg or f"HTTP {r.status_code}")
    return body.get("data")


# ---------- کاربر ----------
async def get_user(chat_id):
    """کاربر را با chat_id برمی‌گرداند یا None."""
    return await _call("GET", f"/bot/users/by-chat/{chat_id}", allow_404=True)


async def link_phone(chat_id, phone):
    """اگر شماره در سیستم باشد chat_id را به آن کاربر وصل می‌کند؛ وگرنه None."""
    return await _call(
        "POST", "/bot/link-phone", data={"chat_id": chat_id, "phone": phone},
        allow_404=True,
    )


async def register(chat_id, full_name, grade, major, phone=""):
    return await _call(
        "POST", "/bot/register",
        data={"chat_id": chat_id, "full_name": full_name, "grade": grade,
              "major": major, "phone": phone},
    )


# ---------- دانش‌آموز ----------
async def send_report(chat_id, text, file=None):
    return await _call(
        "POST", "/bot/reports", data={"chat_id": chat_id, "text": text}, file=file
    )


async def week_report(chat_id):
    return await _call("GET", "/bot/reports/week", params={"chat_id": chat_id})


# ---------- پشتیبان ----------
async def inbox(chat_id):
    return await _call("GET", "/bot/inbox", params={"chat_id": chat_id})


async def thread(chat_id, thread_id):
    return await _call(
        "GET", f"/bot/threads/{thread_id}", params={"chat_id": chat_id}
    )


async def send_reply(chat_id, thread_id, text, file=None):
    return await _call(
        "POST", f"/bot/threads/{thread_id}/reply",
        data={"chat_id": chat_id, "text": text}, file=file,
    )


async def broadcast(chat_id, scope, text, file=None):
    """scope: 'no_report' (فقط بدون گزارش امروز) یا 'all'"""
    return await _call(
        "POST", "/bot/broadcast",
        data={"chat_id": chat_id, "scope": scope, "text": text}, file=file,
    )


# ---------- صف اعلان‌ها (به‌جای cron) ----------
async def outbox_pending():
    return await _call("GET", "/bot/outbox") or []


async def outbox_ack(item_id, ok=True):
    return await _call(
        "POST", f"/bot/outbox/{item_id}/ack", data={"ok": 1 if ok else 0}
    )
