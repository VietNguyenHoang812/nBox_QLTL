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
    field VARCHAR(255),
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
    path_folder VARCHAR(255),
    pathfile VARCHAR(255)
);

-- Insert sample data
INSERT INTO documents (id, option_doc, doc_name, doc_code, date_publish, date_expire, version, author, aprrover, year_publish, field, doc_type, validity, status, updated_by, leader_approver) VALUES 
    ('VOF300', '1', 'Guideline quy hoạch mạng lõi', 'GL.CNVTQĐ.KT.01', '2023-10-25', '2025-10-25', '1', 'vinhnnq', 'vudx', '2023', 'Mạng lõi', '2', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('FAQ001', '2', 'FAQ mảng Vô tuyến', '', '', '', '', '', 'vietnh41', '', '1', '', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('4', '3', 'Trường điện từ', 'FAKECODE001', '1999-12-01', '2099-12-31', '9', 'vietnh41', 'vietnh41', '1999', 'Vô tuyến', '2', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41'),
    ('HDS002', '4', 'Tài liệu hướng dẫn sử dụng vDCIM', 'BM.18.QT.09.QLCL.03', '2024-09-27', '2026-09-27', '1', 'hiennt', 'hienltm', '2024', 'Ứng dụng CNTT', '2', 'Mới nhất', 'Đã tiếp nhận', 'vietnh41', 'vietnh41');

INSERT INTO files (id, doc_id, file_name, file_format, file_role, created_at, updated_at, updated_by, path_folder, pathfile) VALUES 
    ('VOF300_VB', 'VOF300', 'Guideline QH CORE', 'pdf', 'VB', '2025-06-23 17:07:00', '2025-06-23 17:07:00', 'vietnh41', 'aws2/netmind/category_file_upload/sample/Guideline QH CORE.pdf', 'Guideline QH CORE.pdf'),
    ('VOF300_PT', 'VOF300', 'Ph Tr_GL Quy hoach Core', 'pdf', 'PT', '2025-06-23 17:07:00', '2025-06-23 17:07:00', 'vietnh41', 'aws2/netmind/category_file_upload/sample/Ph Tr_GL Quy hoach Core.pdf', 'Ph Tr_GL Quy hoach Core.pdf'),
    ('FAQ001_VB', 'FAQ001', 'FAQ Vô tuyến', 'xlsx', 'VB', '2025-06-23 17:07:00', '2025-06-23 17:07:00', 'vietnh41', 'aws2/netmind/category_file_upload/sample/FAQ Vô tuyến.xlsx', 'FAQ Vô tuyến.xlsx'),
    ('4_FAKEEE', '4', 'Trường điện từ', 'txt', 'VB', '2025-06-23 17:07:00', '2025-06-23 17:07:00', 'vietnh41', 'aws2/netmind/category_file_upload/sample/Trường điện từ.txt', 'Trường điện từ.txt'),
    ('HDS002_VB', 'HDS002', 'HDSD_DCIM_v1.0', 'docx', 'VB', '2025-06-23 17:07:00', '2025-06-23 17:07:00', 'vietnh41', 'aws2/netmind/category_file_upload/sample/HDSD_DCIM_v1.0.docx', 'HDSD_DCIM_v1.0.docx');