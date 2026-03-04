# 🅿️ Brno Smart Park: AI-Powered Surge Pricing pro parkování

**Brno Smart Park** je inovativní platforma pro pronájem parkovacích míst v Brně. Řeší problém nedostatku parkovacích kapacit pomocí **dynamické cenotvorby (surge pricing)**.

Aplikace využívá otevřená data z [data.brno.cz](https://data.brno.cz/) (historická a aktuální obsazenost parkovišť) a pomocí strojového učení predikuje poptávku v čase a prostoru. Když AI detekuje blížící se nedostatek míst v určité lokalitě, automaticky navýší cenu, čímž motivuje řidiče využít okrajovější parkoviště, a naopak.

## 🚀 Technologie
* **Backend:** FastAPI (Python)
* **Frontend:** Streamlit (Python)
* **AI / ML:** Scikit-learn (Random Forest Regressor pro predikci obsazenosti)
* **CI/CD:** GitHub Actions pro automatické nasazení na Render.com

---

## 💻 Jak spustit projekt lokálně

Pro běh projektu potřebuješ mít nainstalovaný **Python 3.9+**.

### 1. Stažení a příprava prostředí
Nejprve si naklonuj repozitář a vytvoř virtuální prostředí, ať si "nezaplevelíš" systémový Python:

```bash
git clone [https://github.com/TVUJ_UCET/brno-smart-park.git](https://github.com/TVUJ_UCET/brno-smart-park.git)
cd brno-smart-park

# Vytvoření a aktivace virtuálního prostředí
python -m venv venv

# Windows aktivace:
venv\Scripts\activate
# Mac/Linux aktivace:
source venv/bin/activate

# Instalace závislostí
pip install -r requirements.txt