# serverSystem-Lab2-Del2

Detta projekt omfattar nätverkskonfiguration, systemadministration och automatisering av en servermiljö i Proxmox för domänen `dubai.lab`. Miljön körs på VLAN 2024 med det interna nätverket `172.31.24.0/24`.

## Projektöversikt
Projektet är uppdelat i två huvudmoment:
- **Del A:** Inventering och rapportgenerering via Python-script (`rapport.json`).
- **Del B:** Konfigurationshantering och automatisering av virtuella maskiner med Ansible.

## Förutsättningar
All automation utförs från kontrollnoden `Ansible-admin` som kör Debian 13.

### 1. SSH-konfiguration
För att Ansible ska kunna kommunicera med Proxmox-noden (`172.31.24.30`) krävs lösenordslös inloggning:
1.  **Generera nyckel:** `ssh-keygen -t ed25519`
2.  **Kopiera till Proxmox:** `ssh-copy-id root@172.31.24.30`
3.  **Verifiera anslutning:** `ssh root@172.31.24.30`

### 2. Installation av beroenden
Kör följande kommandon på kontrollnoden:
```bash
sudo apt update
sudo apt install ansible python3-yaml -y

```

## Ansible Körningskommandon

Beroende på vilket test- eller driftsläge som önskas används följande kommandon i terminalen:

* **Normal körning** (Utför ändringarna skarpt på måldatorerna):
```bash
ansible-playbook playbook.yaml

```


* **Dry-run / Check** (Testkör skriptet och visar vad som skulle ändras):
```bash
ansible-playbook playbook.yaml --check

```


* **Check och Diff** (Dry-run som även visar exakta radskillnader i konfigurationen):
```bash
ansible-playbook playbook.yaml --check --diff

```



## Mappstruktur

Projektet är organiserat enligt följande för att främja modularitet:

* `ansible.cfg`: Central konfiguration som sätter inventory-sökväg och inaktiverar `host_key_checking`.
* `inventory/hosts.ini`: Definition av Proxmox-noder (vår array av maskiner).
* `proxmox.yaml`: Huvud-playbook som styr körningen och anropar tasks.
* `desired_state/main.yaml`: Innehåller definitionen av det önskade tillståndet för miljön.
* `log/`: Innehåller loggfiler som `inventory.log` och `warning.log`.

Mappstrukturen framställdes genom en iterativ process med hjälp av AI. Genom att mata in specifik information om projektets omfattning, vilka mappar som krävdes och vilka specifika *tasks* som skulle genomföras, genererades flera olika bild versioner. 

För att nå det slutgiltiga resultatet krävdes en mer detaljerad och preciserad beskrivning i prompten gällande exakt vilka undermappar och filer som behövdes för att stödja projektets logik. Arbetet fortsatte tills vi uppnådde denna specifika struktur, vilken vi fastställde som den mest optimala för att organisera våra Ansible-playbooks och tillhörande konfigurationsfiler på ett logiskt och lätthanterligt sätt. Nedan kan man se den Mappstrukturen som vi valde:

<img width="908" height="496" alt="image" src="https://github.com/user-attachments/assets/91a530b3-f80c-4928-ac23-d92ba7e8dfa8" />


## Felhantering & Testning

För att verifiera systemets förmåga att logga varningar har vi simulerat ett fel genom att låsa en virtuell maskin i backup-läge:

```bash
# Kommando för att låsa en VM (t.ex. ID 100)
qm set 100 --lock backup

```

Detta gör att Ansible inte kan starta maskinen, vilket fångas upp av vår felhanteringslogik (via en loop i summary) och skrivs till `warning.log`.

## Idempotens

Systemet är designat för att vara **idempotent**. Vid en andra körning i rad av samma playbook ska inga nya ändringar ske (`changed=0`), vilket bekräftar att systemet känner av att det redan befinner sig i det önskade tillståndet.

---


