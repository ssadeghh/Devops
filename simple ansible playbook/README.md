# Ansible Nginx Setup with Custom Page

This project demonstrates how to use **Ansible** to install and configure **Nginx** on remote servers and deploy a custom HTML page.

---

## Project Structure
```bash
├── files
│ └── index.html # Custom HTML page to serve
├── inventory # Inventory file with target hosts
└── nginx-setup.yml # Ansible playbook for Nginx setup
```

### Usage
Test connectivity to the target servers:

```bash
ansible all -i inventory -m ping
```

Run the playbook:

```bash
ansible-playbook -i inventory nginx-setup.yml
```

Access the custom page:
Open a web browser and visit the target server IP (e.g., ```http://192.168.150.129```).