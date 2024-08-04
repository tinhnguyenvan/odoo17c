# Option 1
    - run:  docker-compose up -d
    - Link: 127.0.0.1:8069

    - Neu tao domain odoo.test
      - Copy file folder config/nginx.conf
          - Note: file nginx co dung ssl
      - Add file host /etc/hosts => odoo.test

# Option 2
    - Chạy truc tiep:
        - install: pip install --upgrade pip && pip install -r requirements.txt
        - start: ./odoo-bin -c /etc/odoo/odoo-c.conf