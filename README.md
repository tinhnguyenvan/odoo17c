# CACH 1
    - run:  docker-compose up -d
    - Link: 127.0.0.1:8069

# CACH 2
    - Chạy truc tiep:
        - install: pip install --upgrade pip && pip install -r requirements.txt
        - start: ./odoo-bin -c /etc/odoo/odoo-c.conf