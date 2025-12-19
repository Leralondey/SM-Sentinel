# Rapport de Veille XSD du 19/12/2025 11:18

### 🔄 Comparaison de Versions
| Ancienne Version | Nouvelle Version |
| :--- | :--- |
| `repository_prod_161025.zip` | `repository_prod_121225.zip` |

## Résumé Global
```text
commit 014a2bbe0c25eaf1fe975199c6d0e6485ebc5c7b
Author: SM-Sentinel Bot <bot@sm-sentinel.local>
Date:   Fri Dec 19 11:18:14 2025 +0100

    Auto-update schemas: 2025-12-19 11:18:14 | Source: repository_prod_121225.zip

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
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000101/7/eahv-iv-2015-000101-7-2.xsd`<br>💡 *En tant qu'analyste d'affaires spécialisé eCH, voici l'impact métier de l'introduction de ce nouveau schéma XSD :

*   **Nouvelle exigence de standardisation pour les annonces APG :** Ce nouveau schéma (`eahv-iv-2015-000101-7-2.xsd`) définit une structure XML standardisée et obligatoire pour les "Annonces initiales de prestation APG". Cela signifie que toute communication électronique concernant une nouvelle demande d'APG doit désormais impérativement respecter ce format.
*   **Données clés rendues obligatoires et structurées :** Le champ `businessProcessId` devient obligatoire et doit suivre un modèle précis (`\d{3}\.\d{3}\..*`), passant d'une potentielle saisie libre à un identifiant structuré et validé. De plus, l'attribut `minorVersion` ainsi que les sections `header` et `content` du message deviennent des éléments fondamentaux à fournir.
*   **Adaptations techniques nécessaires :** Les systèmes informatiques des acteurs (expéditeurs et récepteurs) impliqués dans le processus APG devront être mis à jour pour générer ou traiter des messages XML conformes à ce nouveau schéma, garantissant la présence et la validité de toutes les nouvelles données requises.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000301/7/eahv-iv-2015-000301-7-2.xsd`<br>💡 *En tant qu'Analyste Métier spécialisé eCH, voici l'impact business de l'introduction de ce nouveau schéma XSD :

*   **Création d'un nouveau processus de correction :** Ce schéma introduit un nouveau type de message XML pour la "correction d'une annonce de paiement rétroactif" (compte 214.3060). Tous les systèmes émetteurs devront désormais être capables de générer et d'envoyer ce nouveau type de message pour gérer ces corrections spécifiques, avec un `header`, un `content` et une `minorVersion` obligatoires.
*   **Nouvelles données obligatoires et formatées :** Le champ `businessProcessId` dans l'en-tête du message devient obligatoire. Il devra impérativement suivre un format numérique de 18 chiffres, ce qui exigera une gestion précise de cette identification dans les systèmes d'information.
*   **Renforcement de la qualité et de la standardisation des données :** L'utilisation généralisée de types de données spécifiques issus des normes eCH (`eCH-0044f`, `eCH-0058`) et des types `common` pour de nombreux champs (comme `svnr`, `companyId`, `billingYear`, `correctionAmount`) impose une validation plus stricte des données et garantit une plus grande cohérence et interopérabilité entre les systèmes.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000401/7/eahv-iv-2015-000401-7-2.xsd`<br>💡 *En tant qu'analyste métier spécialisé eCH, voici l'impact commercial de cette mise à jour du schéma XSD pour les "Annonces de rectification pour restitution" (compte 214.4609) :

*   **Données désormais obligatoires :** L'attribut `minorVersion` au niveau du message racine et l'élément `businessProcessId` dans l'en-tête deviennent des champs obligatoires. Cela signifie que les systèmes émetteurs devront impérativement fournir ces informations dans chaque message de correction, ce qui n'était potentiellement pas le cas auparavant.
*   **Validation des données renforcée :** Le type de l'identifiant du processus métier (`businessProcessId`) n'est plus une simple chaîne de caractères mais un type de données contraint. Cela implique une validation plus stricte des valeurs acceptées, réduisant les erreurs et garantissant une meilleure qualité des données transmises.
*   **Impact sur l'intégration des systèmes :** Les partenaires et systèmes émetteurs ou consommateurs de ces messages devront adapter leurs interfaces pour inclure systématiquement les nouvelles données obligatoires et respecter les formats précis des types de données mis à jour. Cela vise à améliorer la traçabilité et la fiabilité des corrections de restitution.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000501/7/eahv-iv-2015-000501-7-2.xsd`<br>💡 *En tant qu'analyste métier spécialisé eCH, voici l'impact business de l'introduction de ce nouveau schéma XSD :

*   **Données obligatoires introduites :** Le nouveau protocole de traitement (`000501`) exige désormais la présence obligatoire de l'en-tête (`header`) et de l'attribut `minorVersion` dans tous les messages. Les systèmes émetteurs devront s'assurer que ces informations sont toujours fournies pour que le message soit valide.
*   **Restriction stricte du type de message :** Le champ `subMessageType` est dorénavant limité à la valeur fixe `000501`. Cette contrainte garantit que le message est exclusivement utilisé pour les "protocoles de traitement", renforçant ainsi la clarté et la conformité des échanges de données.
*   **Nouveau standard d'échange :** L'introduction de ce schéma définit un nouveau standard structuré pour l'échange des "protocoles de traitement" dans le cadre eAHV-IV. Tous les acteurs impliqués devront adapter leurs applications pour produire et consommer des messages conformes à cette structure et à ses contraintes, afin d'assurer l'interopérabilité.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-000601/7/eahv-iv-2015-000601-7-2.xsd`<br>💡 *En tant qu'Analyste Métier spécialisé eCH, voici l'impact métier de cette nouvelle version du schéma (v7.2) :

*   **Standardisation et complétude des messages :** Des éléments clés de la structure du message, tels que l'en-tête (`header`), le contenu (`content`) et l'attribut de version mineure (`minorVersion`), deviennent obligatoires. Les systèmes émetteurs devront systématiquement fournir ces informations de base, assurant ainsi une meilleure complétude et un traitement plus fiable des messages de type "État du registre" (000601).

*   **Validation des données renforcée :** Des champs importants, comme l'identifiant du message de référence (`referenceMessageId`), passent d'un type générique à des types eCH spécifiques (`eCH-0058:messageIdType`), et le `subMessageType` est strictement contraint à la valeur "000601". Ceci impose une validation plus stricte des données échangées, réduisant les erreurs d'intégration et garantissant la conformité aux standards eCH.

*   **Exigences de données accrues pour le contenu :** La section `content` exige désormais la présence de la `declaration` ainsi que des données principales (`masterDataA`, `masterDataB`). Les processus métier émetteurs doivent s'assurer que ces informations sont toujours disponibles et complètes, car elles sont considérées comme essentielles pour le traitement ou l'enregistrement de l'état du registre.* |
| Nouvelle Version | `SM-Client-Atos/xsd_xslt/eahv-iv-2015-common/7/eahv-iv-2015-common-7-2.xsd`<br>💡 *En tant que Business Analyst spécialisé eCH, voici l'impact métier de l'introduction de cette nouvelle version de schéma XSD (7.2) pour les échanges eAHV-IV :

*   **Standardisation Forcée des En-têtes de Messages :** La nouvelle définition stricte des en-têtes de message (`headerBaseType`) rend de nombreux champs (comme l'ID de l'expéditeur, l'ID du destinataire, l'ID du message, etc.) obligatoires et impose des types de données spécifiques. Cela garantit une traçabilité accrue, une identification univoque des communications et une meilleure fiabilité des échanges entre les systèmes.
*   **Contrôle Renforcé sur les Données Métier :** L'introduction de types de données restreints, comme le `maritalStatusType` avec des codes numériques prédéfinis, élimine l'utilisation de texte libre ou de codes non standards. Cela améliore significativement la qualité, la cohérence et l'interopérabilité des données échangées, réduisant les erreurs d'interprétation et de traitement.
*   **Mise à Jour des Systèmes Partenaires Impérative :** En tant que nouvelle version du schéma commun (7.2), tous les systèmes émetteurs et récepteurs d'informations eAHV-IV devront s'adapter à cette définition. Cela implique des validations plus strictes et potentiellement des ajustements dans les processus de collecte ou de génération de données pour assurer la conformité aux nouvelles exigences et la fluidité des échanges.* |
