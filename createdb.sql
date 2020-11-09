create table clients(
    id serial primary key,
    name varchar(255),
    addr varchar(50)
);

create table rooms(
    id serial primary key,
    name varchar(255),
    author_id int references clients(id)
);

create table clients_rooms(
    client_id int references clients(id),
    room_id int references rooms(id)
);

create table messages(
    id serial primary key,
    room_id int references rooms(id),
    from_id int references clients(id),
    to_id int references clients(id),
    date_time timestamp default current_timestamp,
    content varchar(255)
);
