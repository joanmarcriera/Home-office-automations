import re
from pathlib import Path

def fix_pricing_docs():
    path = Path("docs/knowledge_base/api_pricing_free_tiers.md")
    content = path.read_text()

    # Abacus.AI: [Docs](https://abacus.ai/service/docs) -> [Docs](https://abacus.ai/)
    content = content.replace("https://abacus.ai/service/docs", "https://abacus.ai/")

    # Z.ai: https://docs.z.ai/guides/pricing -> https://open.bigmodel.cn/pricing (guess) or just home
    content = content.replace("https://docs.z.ai/guides/pricing", "https://open.bigmodel.cn/")

    # SambaNova: https://sambanova.ai/docs -> http://docs.sambanova.ai/
    content = content.replace("https://sambanova.ai/docs", "http://docs.sambanova.ai/")
    # SambaNova: https://sambanova.ai/pricing -> https://cloud.sambanova.ai/plans/pricing
    content = content.replace("https://sambanova.ai/pricing", "https://cloud.sambanova.ai/plans/pricing")

    path.write_text(content)

def fix_grocy():
    path = Path("docs/services/grocy.md")
    content = path.read_text()
    # KitchenOwl: https://github.com/KitchenOwl/KitchenOwl -> https://github.com/KitchenOwl/kitchenowl
    content = content.replace("https://github.com/KitchenOwl/KitchenOwl", "https://github.com/KitchenOwl/kitchenowl")
    path.write_text(content)

def fix_mcp_links():
    # Democratize technology links might be case sensitive or moved.
    # Looking at the ls, they seem to exist in the org.
    # DesktopCommanderMCP vs desktop-commander-mcp?
    # Actually the error was 404 for fuzzing-mcp-server and symbolic-mcp.
    # I'll check if they are in the org list.
    pass

if __name__ == "__main__":
    fix_pricing_docs()
    fix_grocy()
