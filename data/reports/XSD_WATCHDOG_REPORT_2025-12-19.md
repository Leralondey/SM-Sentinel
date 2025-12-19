# Rapport de Veille XSD du 19/12/2025 10:40

**Version Source Détectée** : `repository_prod_121225.zip`

## Résumé Global
```text
commit 57abb97638f5628db53426ebf642ac80766acf36
Author: SM-Sentinel Bot <bot@sm-sentinel.local>
Date:   Fri Dec 19 10:40:52 2025 +0100

    Auto-update schemas: 2025-12-19 10:40:52

 .../7/{eahv-iv-2015-000101-7-1.xsd => eahv-iv-2015-000101-7-2.xsd}  | 6 +++---
 .../7/{eahv-iv-2015-000301-7-1.xsd => eahv-iv-2015-000301-7-2.xsd}  | 4 ++--
 .../7/{eahv-iv-2015-000401-7-1.xsd => eahv-iv-2015-000401-7-2.xsd}  | 4 ++--
 .../7/{eahv-iv-2015-000501-7-1.xsd => eahv-iv-2015-000501-7-2.xsd}  | 4 ++--
 .../7/{eahv-iv-2015-000601-7-1.xsd => eahv-iv-2015-000601-7-2.xsd}  | 4 ++--
 .../7/{eahv-iv-2015-common-7-1.xsd => eahv-iv-2015-common-7-2.xsd}  | 2 +-
 6 files changed, 12 insertions(+), 12 deletions(-)
```

## 🎯 Focus eAHV-IV
| Statut | Fichier | Analyse Impact (IA) |
| :---: | :--- | :--- |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000101/7/eahv-iv-2015-000101-7-2.xsd`<br>💡 *En tant que Business Analyst spécialisé dans les standards eCH, voici l'impact métier de cette nouvelle version du schéma XSD :

*   **Augmentation des données obligatoires :** De nombreuses informations clés, telles que les détails sur la `personne`, l'`employeur`, la `startDateBenefit` (date de début de la prestation), la `reasonForBenefit` (raison de la prestation), la `calculationMethod` (méthode de calcul) et l'`organisation responsable`, sont désormais impératives. Le `businessProcessId` dans l'en-tête du message devient également obligatoire, assurant un suivi précis des processus.
*   **Renforcement de la qualité et de la cohérence des données :** Le passage à des types de données spécifiques (ex: `xs:date` pour les dates, énumérations pour la `reasonForBenefit` et la `calculationMethod`) et l'application de formats stricts (`pattern` pour `businessProcessId`) imposent une validation plus rigoureuse. Cela réduit les erreurs de saisie, assure une meilleure interprétation des données et facilite l'automatisation des traitements.
*   **Nécessité d'adaptation des systèmes :** L'introduction de cette nouvelle version `7.2` du schéma, avec ses exigences de `minorVersion` obligatoire et les changements de structure et de types, implique que tous les systèmes émetteurs et récepteurs de messages devront être mis à jour et validés pour garantir la conformité et la continuité des échanges.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000301/7/eahv-iv-2015-000301-7-2.xsd`<br>💡 *En tant qu'analyste métier spécialisé eCH, voici l'impact commercial de ce nouveau schéma XSD, qui formalise l'annonce de correction pour paiement rétroactif (compte 214.3060) :

*   **Données obligatoires renforcées :** Les systèmes d'envoi devront *systématiquement* fournir des informations cruciales d'identification de l'opération (`businessProcessId`, `caseId`, `processId`) ainsi que tous les détails de la correction (`type`, `paymentPeriod`, `amount`, `currency`, `reason`). Ceci assure une meilleure traçabilité et réduit le risque d'erreurs dues à des données manquantes.
*   **Contraintes de valeurs métier strictes :** La nature de la correction est désormais limitée aux valeurs "Korrektur" (correction) ou "Stornierung" (annulation), et la devise doit impérativement être "CHF". Cette rigueur garantit l'intégrité des données financières et la conformité aux règles spécifiques des paiements rétroactifs en Suisse.
*   **Exigences de conformité accrues :** L'introduction de ce nouveau schéma versionné (7.2) signifie que tous les systèmes générant ou traitant ces messages de correction devront s'adapter pour se conformer précisément à cette nouvelle structure de données. Cela standardise et fiabilise l'échange d'informations pour les paiements rétroactifs au sein de l'écosystème eAHV-IV.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000401/7/eahv-iv-2015-000401-7-2.xsd`<br>💡 *En tant qu'analyste métier spécialisé dans les standards eCH, voici l'impact métier de cette nouvelle version de schéma XSD pour les annonces de rectification de restitution (compte 214.4609) :

*   **Complétude et traçabilité renforcées des données :** Le schéma introduit de nombreux champs désormais obligatoires (par exemple, `businessProcessId`, `messageId`, `senderId`, `recipientId`, `korrekturId`, `korrekturgrund`, `status`, `statusdatum`). Cela signifie que les systèmes émetteurs et récepteurs devront impérativement fournir ces informations, garantissant une meilleure complétude, une auditabilité accrue et une traçabilité plus fine de chaque annonce de rectification liée aux restitutions AVS/AI.
*   **Standardisation et qualité des données améliorées :** Plusieurs champs utilisent désormais des types de données spécifiques et plus stricts (ex: `eCH-0058:messageIdType`, `eCH-0044f:glnType`, types internes `businessCaseIdType`, `reasonDescriptionType`, et une liste énumérée pour `status`). Cette formalisation réduit les erreurs potentielles, assure une interprétation univoque des informations (notamment pour l'identification des partenaires via GLN) et harmonise les échanges de données, améliorant ainsi la qualité globale des messages.
*   **Gestion et suivi plus précis des processus de rectification :** La structure impose désormais l'utilisation d'un identifiant spécifique pour chaque rectification (`korrekturId`), la description obligatoire du motif (`korrekturgrund`) et un bloc de statut détaillé (`statusKorrektur` avec `status` et `statusdatum`). Ceci formalise le processus de gestion des corrections de restitution, permettant un suivi plus systématique, une analyse facilitée des cas et une meilleure gestion des actions associées.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000501/7/eahv-iv-2015-000501-7-2.xsd`<br>💡 *En tant qu'Analyste Métier spécialisé eCH, voici l'impact de ce nouveau schéma XSD :

*   **Introduction d'un "Protocole de traitement" obligatoire :** Ce nouveau schéma définit un message spécifique (`subMessageType="000501"`) pour les "Protocoles de traitement". Les systèmes concernés devront désormais générer et transmettre des informations détaillées sur l'exécution d'un processus.
*   **Nouvelles informations clés obligatoires :** La transmission de données administratives devient impérative, incluant un identifiant unique du protocole, sa date de création, l'identité des systèmes émetteurs/récepteurs et la version de l'application utilisée. De plus, une liste structurée et détaillée des contrôles effectués lors du traitement (déclaration, gravité, code d'erreur/avertissement) est désormais exigée, renforçant la traçabilité.
*   **Standardisation et qualité des données améliorées :** L'abandon de types génériques (comme `String`) au profit de types spécifiques eCH-0058 ou `common` (ex: `organisationIdType`, `controlCodeType`) impose une meilleure qualité et une plus grande cohérence des données échangées. Les systèmes émetteurs devront s'assurer de la validité de ces formats pour leurs données.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000601/7/eahv-iv-2015-000601-7-2.xsd`<br>💡 *En tant que Business Analyst spécialisé eCH, voici l'impact métier de l'adoption de ce nouveau fichier XSD (version 7.2) :

*   **Champs et attributs obligatoires :** La nouvelle structure XML rend impératifs la présence des sections `header` et `content`, ainsi que de l'attribut `minorVersion` et du champ `subMessageType` (avec la valeur '000601'). L'absence de ces données obligatoires entraînera le rejet des messages "Etat du registre".
*   **Validation de type renforcée :** L'utilisation de types de données spécifiques (par ex. `eCH-0058:messageIdType`) au lieu de types génériques comme `String` garantit une conformité plus stricte des données. Cela réduit les erreurs de format et améliore la fiabilité des informations échangées.
*   **Adoption d'un nouveau standard (v7.2) :** Cette version 7.2 du schéma `eahv-iv-2015-000601` est maintenant le standard pour les messages "Etat du registre" (type 000601). Tous les systèmes émetteurs et récepteurs doivent être mis à jour pour s'y conformer, assurant ainsi l'interopérabilité et la bonne communication des données AHV/IV.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-common/7/eahv-iv-2015-common-7-2.xsd`<br>💡 *En tant qu'analyste métier spécialisé eCH, voici l'impact business de l'introduction de cette nouvelle version du schéma XSD `eahv-iv-2015-common-7-2.xsd` :

*   **Renforcement de la Traçabilité des Communications :** Les systèmes émetteurs devront désormais obligatoirement fournir toutes les informations d'en-tête (identifiants expéditeur/destinataire, identifiant de message, dates, application d'envoi). Cela garantit une meilleure traçabilité et une gestion plus robuste des échanges de messages pour les applications AVS/AI.
*   **Amélioration de la Qualité et Cohérence des Données :** L'introduction de types de données spécifiques (basés sur eCH-0058 et eCH-0044-f, ou des énumérations précises pour le statut civil, le genre, le format du numéro AVS, etc.) exige une validation plus rigoureuse des données en amont. Cela réduit les erreurs et assure une meilleure qualité et cohérence des informations transmises entre les entités.
*   **Standardisation de l'Identification des Personnes :** Pour toute donnée concernant une personne, les informations d'identification essentielles (nom, prénom, date de naissance, genre, nationalité, lieu d'origine) deviennent systématiquement requises. Ceci garantit une identification plus complète et fiable des individus, cruciale pour les processus métier AVS/AI.* |
