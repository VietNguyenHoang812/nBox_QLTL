-- Create tables
CREATE TABLE documents (
    id VARCHAR(255) PRIMARY KEY,
    option_doc VARCHAR(255) NOT NULL,
    doc_name VARCHAR(255) NOT NULL,
    doc_code VARCHAR(255),
    date_publish VARCHAR(255),
    date_expire VARCHAR(255),
    version VARCHAR(255),
    author VARCHAR(255),
    aprrover VARCHAR(255),
    year_publish VARCHAR(255),
    field VARCHAR(16),
    doc_type VARCHAR(16),
    validity VARCHAR(255),
    status VARCHAR(255),
    updated_by VARCHAR(255),
    leader_approver VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE files (
    id VARCHAR(255) PRIMARY KEY,
    doc_id VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_format VARCHAR(255),
    file_role VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(255),
    pathfolder VARCHAR(255),
    pathfile VARCHAR(255),
);

-- Insert sample data
INSERT INTO documents (id, option_doc, doc_name, doc_code, date_publish, date_expire, version, author, aprrover, year_publish, field, doc_type, validity, status, updated_by, leader_approver) VALUES 
    ('1', '1', 'Quy định OLA, WLA cho Quy trình Bảo dưỡng Ngăn ngừa (PvM)', 'QT.VTNet.VHKT.02', '2024-10-01', '2025-10-01', '9', 'vietnh41', 'vietnh41', '2018', '5', '2', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('2', '1', 'Quy trình Quản lý Sự cố (IM)', 'QT.VTNet.VHKT.04', '2024-10-01', '2025-10-01', '9', 'vietnh41', 'vietnh41', '2018', '3', '4', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('3', '2', 'FAQ mảng Vô tuyến', '', '', '', '', '', 'vietnh41', '', '1', '', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('4', '3', 'Trường điện từ', 'QT.VTNet.VHKT.02', '2024-10-01', '2025-10-01', '9', 'vietnh41', 'vietnh41', '2018', '5', '2', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('5', '4', 'Quy định OLA, WLA cho Quy trình Bảo dưỡng Ngăn ngừa (PvM)', 'QT.VTNet.VHKT.02', '2024-10-01', '2025-10-01', '9', 'vietnh41', 'vietnh41', '2018', '5', '2', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),;

INSERT INTO files (user_id, title, content) VALUES 
    (1, 'First Post', 'This is my first post!'),
    (2, 'Hello World', 'Welcome to my blog!');