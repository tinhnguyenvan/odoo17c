import os
from odoo.service import db
from datetime import datetime

# Đường dẫn lưu backup
backup_path = '/mnt/backup'

# Tên database
db_name = 'odoo'

# Tạo tên file backup
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_file = os.path.join(backup_path, f'{db_name}_{timestamp}.zip')

# Backup database
with open(backup_file, 'wb') as f:
    db.dump_db(db_name, f)
