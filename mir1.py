import os
import requests
import base64
import sys
import time
from threading import Thread

# --- ANSI цвета ---
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
MAGENTA= "\033[95m"
BLUE   = "\033[94m"

# ─────────────────────────────────────────────
# Настройки
# ─────────────────────────────────────────────
OUTPUT_FILE   = "configs/all_configs.txt"
REQUEST_TIMEOUT = 12          # секунды
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ConfigCollector/1.0)"
}

URLS = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/trojan.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ss.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ssr.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ssr.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/trojan.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/hysteria2.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/vmess.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/vless.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/trojan.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/ss.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/ss.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/trojan.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/vless.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/vmess.txt",
    "https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/all_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vmess_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/trojan_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/ssr_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/ss_configs.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/app/sub.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_1.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_2.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_3.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_4.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/mixed",
    "https://raw.githubusercontent.com/onlymeoneme/v2ray_subs/refs/heads/main/list.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/refs/heads/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/ndnode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/nodefree.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/v2rayshare.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/nodev2ray.txt",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/refs/heads/main/sub/share/vless",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/refs/heads/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/refs/heads/master/list.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/lite/subscriptions/xray/normal/mix",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
    "https://raw.githubusercontent.com/Rayan-Config/C-Sub/refs/heads/main/configs/proxy.txt",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
    "https://raw.githubusercontent.com/Everyday-VPN/Everyday-VPN/main/subscription/main.txt",
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/reality",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/ss",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/trojan",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/tuic",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/vless",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/vmess",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/xhttp",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_SS%2BAll_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/refs/heads/main/githubmirror/new/all_new.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/vmess.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/vless.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/trojan.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/shadowsocks.txt",
]

# ─────────────────────────────────────────────
# Утилиты
# ─────────────────────────────────────────────

def is_ci() -> bool:
    """Возвращает True, если скрипт запущен в CI (GitHub Actions)."""
    return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"


def animate_loading(stop_event: dict):
    """Спиннер — показывается только в интерактивном терминале."""
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stop_event["done"]:
        sys.stdout.write(f"\r{CYAN}[ {chars[i % len(chars)]} Сбор... ]{RESET} ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1


def shorten_url(url: str) -> str:
    parts = url.split("/")
    if len(parts) > 4:
        return f"{parts[3]}/.../{parts[-1]}"
    return url[-40:]


def get_mirror_urls(original_url: str) -> list[str]:
    """Прямая ссылка + JSDelivr CDN-зеркала для raw.githubusercontent.com."""
    urls = [original_url]

    if "raw.githubusercontent.com" in original_url:
        p = original_url.split("/")
        if len(p) >= 7:
            user, repo, branch = p[3], p[4], p[5]
            file_path = "/".join(p[6:])
            urls.append(f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{file_path}")
            urls.append(f"https://fastly.jsdelivr.net/gh/{user}/{repo}@{branch}/{file_path}")

    elif "github.com" in original_url and "/raw/" in original_url:
        p = original_url.split("/")
        if len(p) >= 8:
            user, repo, branch = p[3], p[4], p[6]
            file_path = "/".join(p[7:])
            urls.append(f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{file_path}")
            urls.append(f"https://fastly.jsdelivr.net/gh/{user}/{repo}@{branch}/{file_path}")

    return urls


def decode_content(raw: str) -> tuple[list[str], str]:
    """
    Определяет тип контента и возвращает (список конфигов, тип).
    Типы: 'Plain', 'Base64', 'Empty', 'B64_Err'
    """
    content = raw.strip()
    if not content:
        return [], "Empty"

    # Если в тексте есть хотя бы один протокол — это Plain-текст
    if "://" in content:
        lines = [l.strip() for l in content.splitlines() if l.strip() and "://" in l]
        return lines, "Plain"

    # Иначе пробуем Base64
    try:
        padding = len(content) % 4
        if padding:
            content += "=" * (4 - padding)
        decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = [l.strip() for l in decoded.splitlines() if l.strip() and "://" in l]
        return lines, "Base64"
    except Exception:
        return [], "B64_Err"


def fetch_url(url: str) -> str | None:
    """Загружает URL, возвращает текст или None при ошибке."""
    for mirror in get_mirror_urls(url):
        try:
            r = requests.get(mirror, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            r.raise_for_status()
            return r.text
        except requests.RequestException:
            continue
    return None


def parse_configs(url: str) -> tuple[list[str], str]:
    """Загружает и декодирует конфиги из одного URL."""
    in_ci = is_ci()

    stop_event = {"done": False}
    spinner = None

    if not in_ci:
        spinner = Thread(target=animate_loading, args=(stop_event,), daemon=True)
        spinner.start()

    try:
        raw = fetch_url(url)

        stop_event["done"] = True
        if not in_ci:
            sys.stdout.write("\r" + " " * 30 + "\r")

        if raw is None:
            return [], "Net_Err"

        return decode_content(raw)

    except KeyboardInterrupt:
        stop_event["done"] = True
        if not in_ci:
            sys.stdout.write("\r" + " " * 30 + "\r")
        raise
    except Exception:
        stop_event["done"] = True
        if not in_ci:
            sys.stdout.write("\r" + " " * 30 + "\r")
        return [], "Error"


# ─────────────────────────────────────────────
# Главная логика
# ─────────────────────────────────────────────

def main():
    in_ci = is_ci()

    if not in_ci:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{BOLD}{MAGENTA}{'ТИП':<9} | {'КОЛ-ВО':<8} | ИСТОЧНИК{RESET}")
        print(f"{BLUE}" + "-" * 65 + RESET)
    else:
        print("=== Config Collector starting ===")

    # Используем dict для дедупликации с сохранением порядка первого появления
    seen: dict[str, None] = {}
    total_raw = 0

    try:
        for link in URLS:
            configs, data_type = parse_configs(link)
            total_raw += len(configs)

            for cfg in configs:
                seen[cfg] = None   # ключ — сам конфиг, дубликаты игнорируются

            if not in_ci:
                if data_type in ("Plain", "Base64"):
                    type_col = f"{GREEN}{data_type:<9}{RESET}"
                elif data_type == "Empty":
                    type_col = f"{YELLOW}{data_type:<9}{RESET}"
                else:
                    type_col = f"{RED}{data_type:<9}{RESET}"
                print(f"{type_col} | {len(configs):>4} шт.   | {shorten_url(link)}")
            else:
                # В CI — простой лог без ANSI
                print(f"[{data_type}] {len(configs):>4} configs  {shorten_url(link)}")

    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠  Прервано пользователем (Ctrl+C){RESET}")

    finally:
        unique_configs = list(seen.keys())

        # Создаём папку для вывода если нет
        os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs) + "\n")

        if not in_ci:
            print(f"\n{CYAN}╔{'═'*58}╗{RESET}")
            print(f"{CYAN}║{RESET}{BOLD}  ВСЕГО НАЙДЕНО:   {total_raw:<39}{RESET}{CYAN}║{RESET}")
            print(f"{CYAN}║{RESET}{BOLD}  УНИКАЛЬНЫХ:      {len(unique_configs):<39}{RESET}{CYAN}║{RESET}")
            print(f"{CYAN}║{RESET}{BOLD}  СОХРАНЕНО В:     {OUTPUT_FILE:<39}{RESET}{CYAN}║{RESET}")
            print(f"{CYAN}╚{'═'*58}╝{RESET}\n")
        else:
            print(f"\n=== Done ===")
            print(f"Total collected : {total_raw}")
            print(f"Unique configs  : {len(unique_configs)}")
            print(f"Saved to        : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
