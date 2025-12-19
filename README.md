# SM-Sentinel

> *Le gardien automatisé de conformité eCH & SM-Client.*

**SM-Sentinel** surveille en continu les mises à jour silencieuses et les nouvelles versions des schémas XSD du repository Atos. Il couple une détection technique rigoureuse (**Git**) à une analyse **IA (Gemini)** pour traduire instantanément chaque modification de code en impact métier compréhensible.

---

## 🚀 Fonctionnalités Clés

### 1. 🔍 Découverte & Collecte
*   **eCH Standards** : Scanne et télécharge les normes officielles configurées.
*   **Atos SmartClient** : Détecte *automatiquement* la dernière version du bundle ZIP (`repository_prod_ddMMyy.zip`).
*   **Warm Start (Nouveau)** : Au premier lancement, le script récupère automatiquement les **2 dernières versions** pour générer immédiatement un rapport comparatif pertinent, sans attendre la prochaine mise à jour.

### 2. 🧠 Intelligence Artificielle (Gemini 2.5)
Le script ne se contente pas de dire "Le fichier a changé".
*   **Analyse Sémantique** : Il soumet les changements à Gemini pour expliquer *pourquoi* ça change (ex: "Passage d'un champ facultatif à obligatoire", "Nouveau format de date").
*   **Haute Performance** : Les analyses sont parallélisées (5 threads) pour traiter des dizaines de fichiers rapidement.
*   **Mode Hybride** : Si vous n'avez pas de clé API, le script fonctionne quand même (mode dégradé sans analyse textuelle).

### 3. 📊 Rapports Décisionnels
Un rapport Markdown (`.md`) est généré à chaque exécution dans `data/reports/`.
*   **Résumé Global** : Activité sur tout le périmètre.
*   **🎯 Focus eAHV-IV** : Tableau dédié aux schémas critiques avec colonne "Analyse Impact".
*   **Gestion des Versions** : Détecte intelligemment qu'un fichier "Renommé" (`v7-1.xsd` -> `v7-2.xsd`) est en fait une **Mise à jour de version** et déclenche l'analyse dessus.

---

## 🛠️ Installation

1.  **Pré-requis** : Python 3.8+, Git.
2.  **Installation des dépendances** :
    ```powershell
    pip install -r requirements.txt
    ```
    *(Inclut `requests`, `beautifulsoup4`, `google-generativeai`)*

3.  **Renommer la configuration** :
    Copiez `config.example.json` vers `config.json` et ajoutez votre clé API Gemini.
    > 💡 **Obtenir une clé gratuite :** Rendez-vous sur [Google AI Studio](https://aistudio.google.com/) et cliquez sur "Get API key".

---

## ⚙️ Configuration (`config.json`)

```json
{
    "base_dir": "data",
// ...
```

### Détails Configuration
*   **ech_standards** : Séparé en deux sections pour plus de clarté.
    *   `manual` : Ajoutez ici les normes que VOUS voulez suivre spécifiquement.
    *   `auto_discovered` : **Ne touchez pas !** Cette liste est remplie automatiquement par le script lorsqu'il détecte une dépendance eCH dans le ZIP Atos. Cela permet de voir exactement ce que le système a trouvé.
*   **atos_discovery** : Si `true`, le script détecte et télécharge la dernière release Atos.
*   **ai_analysis** : Active l'analyse d'impact métier (Gemini).

---

## ▶️ Utilisation

```powershell
python xsd_watchdog.py
```

### Exemple de Résultat (Rapport)

**Version Source Détectée** : `repository_prod_121225.zip`

📄 **[Voir le rapport complet généré (Exemple réel)](EXAMPLE_REPORT.md)** - Analyse comparative entre une version d'Octobre 2025 et Décembre 2025.

## 🎯 Focus eAHV-IV
| Statut | Fichier | Analyse Impact (IA) |
| :---: | :--- | :--- |
| **Nouvelle Version** | `.../eahv-iv-2015-common-7-2.xsd` | 💡 *En tant qu'analyste métier : L'ajout du type complexe 'commandType' standardise les échanges de commandes...* |
| Modifié | `.../eahv-iv-test.xsd` | 💡 *Le champ 'NewField' devient obligatoire (minOccurs=1)...* |

---

## ❓ FAQ

**Q: L'IA ne se déclenche pas ?**
R: Vérifiez que `enabled` est à `true` et que votre clé est valide. Checkez aussi les logs (`watchdog.log`). L'IA ne se lance que sur les fichiers *Modifiés* ou *Nouvelles Versions* ("Renommés").

**Q: Comment revenir en arrière ?**
R: Tout est stocké dans un vrai dépôt Git local (`data/schemas`). Vous pouvez utiliser toutes les commandes Git (`git log`, `git diff`, `git checkout`) pour explorer l'historique.

**Q: Le script détecte-t-il un changement si le nom du fichier est identique ?**
R: **OUI**. Le système compare le contenu binaire réel ("HASH"). Si Atos modifie une ligne dans un fichier sans changer son nom (Silent Update ou même version affichée), Git le marque comme **M (Modifié)** et l'IA analysera le changement exactement comme pour une nouvelle version.
