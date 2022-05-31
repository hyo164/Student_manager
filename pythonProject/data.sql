  CREATE TABLE user(
  username VARCHAR(20) NOT NULL, 
  password VARCHAR(50) NOT NULL, 
  name VARCHAR(100), 
  prof INT NOT NULL CHECK (prof=1 or prof=2 or prof=3), 
  student_id VARCHAR(4),
  email VARCHAR(50), 
  PRIMARY KEY(username));
  CREATE TABLE class (
  class_id VARCHAR(5) NOT NULL,
  class_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (class_id),
  UNIQUE INDEX class_id_UNIQUE (class_id ASC) VISIBLE);
  CREATE TABLE student (
  student_id VARCHAR(4) NOT NULL,
  student_name VARCHAR(100) NOT NULL,
  username VARCHAR(20) NOT NULL,
  email VARCHAR(50) NULL,
  class_id VARCHAR(45) NOT NULL,
  gender varchar(1) NOT NULL,
  PRIMARY KEY (student_id),
  UNIQUE INDEX student_id_UNIQUE (student_id ASC) VISIBLE,
  UNIQUE INDEX username_UNIQUE (username ASC) VISIBLE,
  FOREIGN KEY (class_id) REFERENCES class(class_id));
  CREATE TABLE subject (
  subject_id VARCHAR(5) NOT NULL,
  subject_name VARCHAR(45) NOT NULL,
  PRIMARY KEY (subject_id),
  UNIQUE INDEX subject_id_UNIQUE (subject_id ASC) VISIBLE);
  CREATE TABLE score (
  id INT NOT NULL AUTO_INCREMENT,
  student_id VARCHAR(4) NOT NULL,
  subject_name VARCHAR(45) NOT NULL,
  subject_id VARCHAR(5) NOT NULL,
  score DECIMAL(2,1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  FOREIGN KEY (student_id) REFERENCES student(student_id),
  FOREIGN KEY (subject_id) REFERENCES subject(subject_id));

  
  
  
    INSERT INTO class (class_id, class_name) VALUES
  ('a1', 'Business management'),
  ('a2', 'Banking'),
  ('a3', 'Accounting');
  INSERT INTO student (student_id, student_name, username, email, class_id, gender) VALUES
  ('0001', 'Nguyen Van A', 'nguyenvana', null, 'a1','M'),
  ('0002', 'Nguyen Van B', 'nguyenvanb', null, 'a2','M'),
  ('0003', 'Nguyen Thi C', 'nguyenthic', null, 'a3','F'),
  ('0004', 'Nguyen Thi D', 'nguyenthid', null, 'a1','F'),
  ('0005', 'Nguyen Van E', 'nguyenvane', null, 'a2','M');
  INSERT INTO subject (subject_id, subject_name) VALUES
  ('Eco','Economics'),
  ('Fin', 'Financial'),
  ('Ban', 'Banking'),
  ('Ins', 'Insurance'),
  ('Bac', 'Basic Accounting');
  INSERT INTO score (student_id, subject_name, subject_id, score) VALUES
  ('0001', 'Ecomomics', 'Eco', 5),
  ('0001', 'Financial', 'Fin', 6.4),
  ('0002', 'Economics', 'Eco', 7.4),
  ('0003', 'Basic Accounting', 'Bac', 4.8),
  ('0004', 'Financial', 'Fin', 5.2),
  ('0004', 'Ecomomics', 'Eco', 6.4);
  INSERT INTO user (username, password, name, prof, student_id) VALUES
  ('nguyenvana', 'a123456', 'Nguyen Van A', 1, '0001'),
  ('nguyenvanb', 'b123456', 'Nguyen Van B', 1, '0001'),
  ('nguyenthic', 'c123456', 'Nguyen Thi C', 1, '0001'),
  ('nguyenthid', 'd123456', 'Nguyen Thi D', 1, '0001'),
  ('nguyenvane', 'e123456', 'Nguyen Van E', 1, '0001'),
  ('tranvanf', 'f123456', 'Tran Van F', 2, ''),
  ('tranvang', 'g123456', 'Tran Van G', 2, ''),
  ('admin', 'admin', '', 3, '');
  


#UPDATE table, other_table
#SET table.col = other_table.other_col
#WHERE table.id = other_table.table_id;
