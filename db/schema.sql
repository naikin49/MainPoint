CREATE TABLE AudioFiles (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    file_name NVARCHAR(255) NOT NULL, 
    file_data VARBINARY(MAX) NOT NULL 
);
CREATE TABLE tgs (
    id INT IDENTITY(1,1) PRIMARY KEY, 
    tg_id NVARCHAR(255) NOT NULL, 
		
);

CREATE TABLE Records (
    id INT IDENTITY(1,1) PRIMARY KEY,               
    file_id INT NOT NULL,                           
    is_poss BIT NOT NULL DEFAULT 0,                 
    score DECIMAL(10, 4) NOT NULL DEFAULT 0.0000,   
    full_text NVARCHAR(MAX) NOT NULL,              
    main_text NVARCHAR(MAX) NOT NULL,              
    tg_id int NULL,             
    CONSTRAINT FK_Records_AudioFiles FOREIGN KEY (file_id) REFERENCES AudioFiles(id),
    CONSTRAINT FK_Records_tgs FOREIGN KEY (tg_id) REFERENCES AudioFiles(id) 
);
