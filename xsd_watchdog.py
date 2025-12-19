#!/usr/bin/env python3
import os
import json
import requests
import subprocess
import shutil
import zipfile
import io
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import concurrent.futures
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('watchdog.log', encoding='utf-8')
    ]
)

class XSDWatchdog:
    def __init__(self, config_path='config.json'):
        self.load_config(config_path)
        self.setup_directories()
        self.configure_git()
        self.configure_ai()

    def configure_git(self):
        self.init_git_repo()
        self.ensure_git_config()

    def ensure_git_config(self):
        # On force la config pour éviter l'erreur "Author identity unknown"
        try:
            subprocess.run(['git', 'config', 'user.email', 'bot@sm-sentinel.local'], cwd=self.schemas_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'SM-Sentinel Bot'], cwd=self.schemas_dir, check=True)
        except Exception as e:
            logging.warning(f"Could not set git config: {e}")

    def init_git_repo(self):
        # On exécute git init de manière idempotente pour réparer si nécessaire
        subprocess.run(['git', 'init'], cwd=self.schemas_dir, check=True)
        logging.info(f"Git repo initialized in {self.schemas_dir}")

    def configure_ai(self):
        """Configure Gemini API if enabled"""
        ai_config = self.config.get('ai_analysis', {})
        if ai_config.get('enabled') and ai_config.get('api_key'):
            try:
                genai.configure(api_key=ai_config['api_key'])
                self.model = genai.GenerativeModel(ai_config.get('model', 'gemini-pro'))
                self.ai_enabled = True
                logging.info("🤖 Gemini AI initialized for report analysis")
            except Exception as e:
                logging.warning(f"Failed to initialize Gemini AI: {e}")
                self.ai_enabled = False
        else:
            self.ai_enabled = False

    def analyze_change_with_ai(self, filename, diff_content, standard_url=None):
        """Ask AI to analyze the business impact of a technical diff"""
        if not self.ai_enabled:
            return None
        if not diff_content.strip():
            logging.warning(f"Empty diff content for {filename}, skipping AI.")
            return None

        logging.info(f"🤖 Sending request to Gemini for {filename} (Diff size: {len(diff_content)} chars)...")

        prompt = f"""
        Act as a Business Analyst specialized in Swiss eGovernment Standards (eCH).
        Analyze the following XSD change (Git diff) and explain the BUSINESS IMPACT in simple terms (French).
        
        Context:
        - File: {filename}
        - Standard Documentation: {standard_url if standard_url else "Internal Technical Schema (No public doc)"}
        
        Focus on:
        1. New constrained fields (minOccurs 0 -> 1).
        2. Type changes (String -> Specific Type).
        3. New mandatory data.
        
        Keep it concise (max 3 bullet points).
        
        Technical Diff:
        {diff_content[:3000]}  # Truncate to avoid token limit
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logging.error(f"AI Analysis failed for {filename}: {e}")
            return None

    def load_config(self, config_path):
        self.config_path = config_path # Store for saving later
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.base_dir = self.config.get('base_dir', 'data')
        self.schemas_dir = os.path.join(self.base_dir, 'schemas')

    def setup_directories(self):
        if not os.path.exists(self.schemas_dir):
            os.makedirs(self.schemas_dir)
        self.init_git_repo()
        self.ensure_git_config()

    def fetch_ech_standard(self, standard_id, url):
        logging.info(f"Checking eCH standard: {standard_id}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Logique de scraping simplifiée
            xsd_links = []
            for a in soup.find_all('a', href=True):
                if a['href'].endswith('.xsd'):
                    xsd_links.append(a['href'])
            
            if not xsd_links:
                logging.warning(f"No XSD found for {standard_id}")
                return

            standard_dir = os.path.join(self.schemas_dir, standard_id)
            if not os.path.exists(standard_dir):
                os.makedirs(standard_dir)

            for link in set(xsd_links): 
                filename = os.path.basename(link)
                full_url = link if link.startswith('http') else f"https://www.ech.ch{link}"
                
                logging.info(f"Downloading {filename}...")
                r = requests.get(full_url)
                if r.status_code == 200:
                    with open(os.path.join(standard_dir, filename), 'wb') as f:
                        f.write(r.content)
                else:
                    logging.error(f"Failed to download {full_url}")

        except Exception as e:
            logging.error(f"Error processing {standard_id}: {str(e)}")

    def fetch_zip_source(self, source_name, url):
        logging.info(f"Processing ZIP source: {source_name}")
        try:
            logging.info(f"Downloading ZIP from {url}...")
            response = requests.get(url)
            response.raise_for_status()
            
            target_base_dir = os.path.join(self.schemas_dir, source_name)
            
            # 1. Clean destination to ensure exact sync (deletions will be detected by git)
            if os.path.exists(target_base_dir):
                shutil.rmtree(target_base_dir)
            os.makedirs(target_base_dir)

            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                for file_info in z.infolist():
                    if file_info.is_dir():
                        continue
                        
                    # Normalize Path: Find 'xsd_xslt' and anchor there
                    # Ex: "repository_prod_161025/xsd_xslt/foo.xsd" -> "xsd_xslt/foo.xsd"
                    # Ex: "xsd_xslt/foo.xsd" -> "xsd_xslt/foo.xsd"
                    original_path = file_info.filename
                    
                    if 'xsd_xslt' in original_path:
                        # Split and keep part starting from xsd_xslt
                        parts = original_path.split('/')
                        try:
                            start_idx = parts.index('xsd_xslt')
                            normalized_path = '/'.join(parts[start_idx:])
                        except ValueError:
                            # Should not happen given the if check, but fallback
                            normalized_path = original_path
                    else:
                        # Fallback for files outside xsd_xslt (if any important ones)
                        # We might want to skip them or keep basename? 
                        # For now, keep basename to avoid huge folder nesting if structure changes completely
                        normalized_path = os.path.basename(original_path)
                        if not normalized_path: continue # Skip root dirs

                    if normalized_path.endswith('.xsd'):
                        target_path = os.path.join(target_base_dir, normalized_path)
                        target_dir = os.path.dirname(target_path)
                        
                        if not os.path.exists(target_dir):
                            os.makedirs(target_dir)
                            
                        with open(target_path, 'wb') as f:
                            f.write(z.read(file_info))
                            
            logging.info(f"Extracted XSDs from {source_name}")

        except Exception as e:
            logging.error(f"Error processing ZIP {source_name}: {str(e)}")

    def sync_local_schemas(self):
        local_source = self.config.get('local_schemas_source')
        if not local_source or not os.path.exists(local_source):
            return # Silent skip if not configured

        logging.info(f"Syncing local schemas from {local_source}")
        target_dir = os.path.join(self.schemas_dir, 'internal_schemas')
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Copie simple des fichiers
        for item in os.listdir(local_source):
            s = os.path.join(local_source, item)
            d = os.path.join(target_dir, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    def commit_changes(self, detected_version=None):
        # Check status
        result = subprocess.run(['git', 'status', '--porcelain'], cwd=self.schemas_dir, capture_output=True, text=True)
        if not result.stdout.strip():
            logging.info("No changes to commit.")
            return

        logging.info("Changes detected. Committing...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(['git', 'add', '.'], cwd=self.schemas_dir, check=True)
        subprocess.run(['git', 'commit', '-m', f"Auto-update schemas: {timestamp}"], cwd=self.schemas_dir, check=True)
        
        # Show stats for console
        diff_stat = subprocess.run(['git', 'show', '--stat', 'HEAD'], cwd=self.schemas_dir, capture_output=True, text=True)
        logging.info("Update Summary:\n" + diff_stat.stdout)

        # Rapport Focus eAHV-IV & Markdown Report
        try:
            # Récupérer la liste des fichiers modifiés dans le dernier commit
            result_files = subprocess.run(['git', 'show', '--name-status', '--format=', 'HEAD'], cwd=self.schemas_dir, capture_output=True, text=True)
            # Output format: "M\tpath/to/file" or "A\tpath/to/file"
            changed_items = result_files.stdout.strip().split('\n')
            
            eahv_changes = []
            for item in changed_items:
                if not item: continue
                parts = item.split('\t')
                status = parts[0]
                filepath = parts[-1]
                if 'eahv-iv' in filepath.lower():
                    eahv_changes.append({'status': status, 'path': filepath})
            
            # --- Console Log Report ---
            if eahv_changes:
                report = "\n" + "="*50 + "\n"
                report += "🔴 FOCUS REPORT: eAHV-IV CHANGES DETECTED\n"
                report += "="*50 + "\n"
                for c in eahv_changes:
                    report += f"- [{c['status']}] {c['path']}\n"
                report += "="*50
                logging.info(report)
            else:
                logging.info("No changes detected in eAHV-IV schemas.")

            # --- Generate Markdown Report ---
            reports_dir = os.path.join(self.base_dir, 'reports')
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            today = datetime.now().strftime("%Y-%m-%d")
            report_filename = f"XSD_WATCHDOG_REPORT_{today}.md"
            report_path = os.path.join(reports_dir, report_filename)
            
            md_content = f"# Rapport de Veille XSD du {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            
            if detected_version:
                md_content += f"**Version Source Détectée** : `{detected_version}`\n\n"
            
            md_content += "## Résumé Global\n"
            md_content += "```text\n"
            md_content += diff_stat.stdout
            md_content += "```\n\n"
            
            md_content += "## 🎯 Focus eAHV-IV\n"
            # Map status codes to emoji/text
            status_map = {'M': 'Modifié', 'A': 'Ajout', 'D': 'Supprimé', 'R': 'Nouvelle Version'}
            # 3. Construction du Tableau Markdown avec Analyse IA
            if eahv_changes:
                # En-tête conditionnel
                if self.ai_enabled:
                    md_content += "| Statut | Fichier | Analyse Impact (IA) |\n| :---: | :--- | :--- |\n"
                else:
                    md_content += "| Statut | Fichier |\n| :---: | :--- |\n"
                
                # --- Préparation Parallel Execution ---
                ai_results = {}
                if self.ai_enabled:
                    analysis_tasks = []
                    for c in eahv_changes:
                        if (c['status'].startswith('M') or c['status'].startswith('R')):
                            try:
                                # Retrieve technical diff
                                diff_proc = subprocess.run(['git', 'diff', 'HEAD^', 'HEAD', '--', c['path']], 
                                                         cwd=self.schemas_dir, capture_output=True, text=True, encoding='utf-8')
                                
                                std_url = None
                                std_url = None
                                # Use helper to search in both manual and auto lists
                                for std in self.get_all_standards():
                                    if std['id'] in c['path']:
                                        std_url = std['url']
                                        break
                                
                                analysis_tasks.append({
                                    'path': c['path'], 
                                    'diff': diff_proc.stdout, 
                                    'url': std_url
                                })
                            except Exception as e:
                                logging.warning(f"Could not prepare diff for {c['path']}: {e}")

                    # Execute AI tasks in parallel
                    if analysis_tasks:
                        logging.info(f"⚡ Starting parallel AI analysis for {len(analysis_tasks)} files...")
                        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                            future_to_path = {
                                executor.submit(self.analyze_change_with_ai, t['path'], t['diff'], t['url']): t['path']
                                for t in analysis_tasks
                            }
                            for future in concurrent.futures.as_completed(future_to_path):
                                path = future_to_path[future]
                                try:
                                    result = future.result()
                                    if result:
                                        ai_results[path] = result
                                except Exception as e:
                                    logging.error(f"AI Analysis task failed for {path}: {e}")

                # --- Build Table ---
                for c in eahv_changes:
                    status_str = status_map.get(c['status'][0], c['status'])
                    path_str = f"`{c['path']}`"
                    
                    if self.ai_enabled:
                        ai_comment = ""
                        if c['path'] in ai_results:
                             ai_comment = f"<br>💡 *{ai_results[c['path']]}*"
                        md_content += f"| {status_str} | {path_str}{ai_comment} |\n"
                    else:
                        md_content += f"| {status_str} | {path_str} |\n"
            else:
                md_content += "> Aucune modification détectée sur le périmètre eAHV-IV.\n"
                
            # Append if file exists (daily log) or write new? 
            # User asked for a file per execution or per day? "XSD_WATCHDOG_REPORT_YYYY-MM-DD.md", imply daily.
            # Let's append if it exists to keep history of the day.
            mode = 'a' if os.path.exists(report_path) else 'w'
            with open(report_path, mode, encoding='utf-8') as f:
                if mode == 'a':
                    f.write("\n\n---\n\n") # Separator for multiple runs same day
                f.write(md_content)
                
            logging.info(f"Markdown report generated: {report_path}")

        except Exception as e:
            logging.error(f"Error generating reports: {e}")

    def discover_atos_versions(self, base_url):
        logging.info(f"Scanning for available versions at {base_url}...")
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            candidates = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                filename = os.path.basename(href)
                if filename.startswith('repository_prod_') and filename.endswith('.zip') and len(filename) == 26:
                    try:
                        date_str = filename[16:22]
                        # Assume DDMMYY format
                        date_obj = datetime.strptime(date_str, "%d%m%y")
                        if not href.startswith('http'):
                            if href.startswith('/'):
                                full_url = f"https://sm-client.atos-solutions.ch{href}"
                            else:
                                full_url = f"https://sm-client.atos-solutions.ch/{href}"
                        else:
                            full_url = href
                        candidates.append({'date': date_obj, 'url': full_url, 'filename': filename})
                    except ValueError:
                        continue

            if not candidates:
                logging.warning("No matching repository_prod_*.zip found.")
                return []

            candidates.sort(key=lambda x: x['date'], reverse=True)
            logging.info(f"Found {len(candidates)} versions. Latest: {candidates[0]['filename']}")
            return candidates

        except Exception as e:
            logging.error(f"Error during discovery: {e}")
            return []

    def get_all_standards(self):
        """Helper to get merged list of manual and auto-discovered standards"""
        # Support default list format for backward compatibility (during transition)
        standards_conf = self.config.get('ech_standards', {})
        if isinstance(standards_conf, list):
            return standards_conf
        
        # New dict format
        return standards_conf.get('manual', []) + standards_conf.get('auto_discovered', [])

    def scan_atos_ech_dependencies(self):
        """Scan Atos folder for eCH dependencies and auto-add them to monitoring (Persistent)"""
        atos_xslt_path = os.path.join(self.schemas_dir, "SM-Client-Atos", "xsd_xslt")
        if not os.path.exists(atos_xslt_path):
            logging.warning("Atos folder not found for eCH dependency scan.")
            return

        logging.info("Scanning Atos dependencies for eCH Standards auto-discovery...")
        found_ech = set()
        
        try:
            for item_name in os.listdir(atos_xslt_path):
                if item_name.startswith("eCH-") and os.path.isdir(os.path.join(atos_xslt_path, item_name)):
                    found_ech.add(item_name)
        except Exception as e:
            logging.error(f"Error scanning Atos dependencies: {e}")
            return

        # Prepare for update
        standards_conf = self.config.get('ech_standards', {})
        
        # Handle migration if still a list
        if isinstance(standards_conf, list):
            logging.info("Migrating configuration to new format (manual/auto_discovered)...")
            standards_conf = {
                "manual": standards_conf,
                "auto_discovered": []
            }
            self.config['ech_standards'] = standards_conf

        manual_ids = {std['id'] for std in standards_conf.get('manual', [])}
        auto_list = standards_conf.get('auto_discovered', [])
        auto_ids = {std['id'] for std in auto_list}
        
        updates_made = False
        for ech_id in found_ech:
            # Add only if not in manual AND not already in auto
            if ech_id not in manual_ids and ech_id not in auto_ids:
                url_id = ech_id.lower() 
                generic_url = f"https://www.ech.ch/fr/ech/{url_id}"
                
                logging.info(f"✨ Auto-discovered new eCH standard: {ech_id}. Persisting to config.")
                auto_list.append({"id": ech_id, "url": generic_url})
                auto_ids.add(ech_id)
                updates_made = True
        
        if updates_made:
            # Save back to file
            try:
                # Reload raw file to preserve formatting? No, json dump is fine.
                # Use self.config_path assuming it was stored. If not, fix main.
                # XSDWatchdog __init__ uses config_path arg but doesn't store it as attribute cleanly?
                # It does: load_config(config_path). Let's check load_config implementation.
                # It doesn't store self.config_path. I will fix that or assume default 'config.json' if passed.
                # Actually I should allow writing back.
                
                # Assume attribute self.config_file exists (added in load_config or init)
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=4)
                logging.info("💾 Configuration updated with new standards.")
            except Exception as e:
                logging.error(f"Failed to save configuration: {e}")

    def execute_cycle(self, atos_version=None):
        """Execute a full update cycle for a specific version state"""
        
        # 1. Atos Download (if version provided)
        if atos_version:
            self.fetch_zip_source("SM-Client-Atos", atos_version['url'])
        
        # 1b. Other ZIP Sources
        for zip_src in self.config.get('zip_sources', []):
            self.fetch_zip_source(zip_src['name'], zip_src['url'])
            
        # 2. Auto-Discovery
        self.scan_atos_ech_dependencies()
        
        # 3. Fetch Standards
        for std in self.get_all_standards():
            self.fetch_ech_standard(std['id'], std['url'])

        # 4. Local Schemas
        self.sync_local_schemas()
        
        # 5. Commit & Report
        ver_name = atos_version['filename'] if atos_version else None
        self.commit_changes(detected_version=ver_name)

    def run(self):
        # Initial check logic
        is_first_run = not os.path.exists(os.path.join(self.schemas_dir, '.git'))
        versions_to_process = []
        
        atos_config = self.config.get('atos_discovery')
        if atos_config and atos_config.get('enabled'):
            available_versions = self.discover_atos_versions(atos_config['url'])
            
            if is_first_run and len(available_versions) >= 2:
                logging.info("🚀 First Run Detected! Executing 'Warm Start' sequence.")
                logging.info(f"Will process previous version ({available_versions[1]['filename']}) then latest ({available_versions[0]['filename']}) to generate comparison.")
                versions_to_process.append(available_versions[1]) # N-1
                versions_to_process.append(available_versions[0]) # N
            elif available_versions:
                versions_to_process.append(available_versions[0]) # Only latest

        if not versions_to_process:
            # Fallback for no atos or manual mode, just run once
            self.execute_cycle()
        else:
            for ver in versions_to_process:
                logging.info(f"▶️ Processing cycle for version: {ver['filename']}")
                self.execute_cycle(atos_version=ver)

if __name__ == "__main__":
    import sys
    config_file = "config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    # ...default config creation logic omitted to keep existing config...
    
    if os.path.exists(config_file):
        watchdog = XSDWatchdog(config_file)
        watchdog.run()
    else:
        print(f"Config file {config_file} not found.")
