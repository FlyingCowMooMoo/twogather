CREATE TABLE boardtask
(
    id INTEGER PRIMARY KEY NOT NULL,
    board_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES task (id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (board_id) REFERENCES taskboard (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX boardtask_board_id ON boardtask (board_id);
CREATE UNIQUE INDEX boardtask_task_id ON boardtask (task_id);
CREATE TABLE color
(
    id INTEGER PRIMARY KEY NOT NULL,
    hex_code TEXT NOT NULL
);
CREATE UNIQUE INDEX color_hex_code ON color (hex_code);
CREATE TABLE employeepin
(
    id INTEGER PRIMARY KEY NOT NULL,
    pin TEXT NOT NULL,
    logo_id INTEGER,
    color_id INTEGER,
    FOREIGN KEY (color_id) REFERENCES color (id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (logo_id) REFERENCES logoimage (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX employeepin_pin ON employeepin (pin);
CREATE UNIQUE INDEX employeepin_logo_id ON employeepin (logo_id);
CREATE UNIQUE INDEX employeepin_color_id ON employeepin (color_id);
CREATE TABLE logo
(
    id INTEGER PRIMARY KEY NOT NULL,
    logo_class TEXT NOT NULL
);
CREATE UNIQUE INDEX logo_logo_class ON logo (logo_class);
CREATE TABLE logoimage
(
    id INTEGER PRIMARY KEY NOT NULL,
    image_name TEXT NOT NULL
);
CREATE UNIQUE INDEX logoimage_image_name ON logoimage (image_name);
CREATE TABLE markedastodo
(
    id INTEGER PRIMARY KEY NOT NULL,
    task_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    marked_at TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employeepin (id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (task_id) REFERENCES task (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX markedastodo_task_id ON markedastodo (task_id);
CREATE UNIQUE INDEX markedastodo_employee_id ON markedastodo (employee_id);
CREATE TABLE role
(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);
CREATE UNIQUE INDEX role_name ON role (name);
CREATE TABLE task
(
    id INTEGER PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    marked_as_task INTEGER NOT NULL,
    marked_as_todo INTEGER NOT NULL,
    marked_as_completed INTEGER NOT NULL,
    assigned_at TEXT NOT NULL,
    updated_at TEXT,
    completed_at TEXT,
    marked_by_id INTEGER,
    marked_as_high_priority INTEGER NOT NULL,
    FOREIGN KEY (marked_by_id) REFERENCES employeepin (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX task_marked_by_id ON task (marked_by_id);
CREATE TABLE taskboard
(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    creator_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES user (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX taskboard_name ON taskboard (name);
CREATE UNIQUE INDEX taskboard_creator_id ON taskboard (creator_id);
CREATE TABLE taskcompletion
(
    id INTEGER PRIMARY KEY NOT NULL,
    task_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employeepin (id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (task_id) REFERENCES task (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX taskcompletion_task_id ON taskcompletion (task_id);
CREATE UNIQUE INDEX taskcompletion_employee_id ON taskcompletion (employee_id);
CREATE TABLE user
(
    id INTEGER PRIMARY KEY NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    active INTEGER NOT NULL,
    confirmed_at TEXT,
    name TEXT NOT NULL
);
CREATE UNIQUE INDEX user_email ON user (email);
CREATE TABLE userroles
(
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role (id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (user_id) REFERENCES user (id) DEFERRABLE INITIALLY DEFERRED
);
CREATE UNIQUE INDEX userroles_user_id ON userroles (user_id);
CREATE UNIQUE INDEX userroles_role_id ON userroles (role_id);